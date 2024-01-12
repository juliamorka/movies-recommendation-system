from collections import defaultdict
from mlxtend.frequent_patterns import apriori, association_rules, fpgrowth, fpmax, hmine
import pandas as pd
from models import Rating


class Recommender:
    def __init__(self, ratings, number_of_clusters):
        self.ratings = ratings
        self.current_cluster = 0
        self.frq_items, self.rules = [], []
        self.liked_movies = ratings.groupby("user")["movie"].apply(list)
        self.recommendations = {i: defaultdict(set) for i in range(1, number_of_clusters + 1)}
        self.new_recommendations = defaultdict(set)

    def create_clusters(self, clusters):
        self.ratings["cluster"] = self.ratings["user"].map({i: clusters.loc[i] for i in range(1, len(clusters) + 1)})

    def update_current_cluster(self, cluster):
        self.current_cluster = cluster
        self.users = self.ratings[self.ratings["cluster"] == cluster]
        self.user_movie_matrix = self.users.groupby(["user", "movie"]).sum()["value"].unstack().fillna(0).astype(
            bool)

    def generate_freq_items(self, algorithm, min_support):
        if algorithm == "apriori":
            self.frq_items = apriori(self.user_movie_matrix, min_support=min_support, use_colnames=True)
        elif algorithm == "fpgrowth":
            self.frq_items = fpgrowth(self.user_movie_matrix, min_support=min_support, use_colnames=True)

    def generate_rules(self, min_confidence):
        self.rules = association_rules(self.frq_items, metric="confidence", min_threshold=min_confidence)

    def generate_recs(self, cluster_strategy):
        if cluster_strategy == "single":
            for user_id in self.users["user"].unique():
                user_liked_movies = self.liked_movies[user_id]
                matching_rules = self.rules[self.rules['antecedents'].apply(lambda x: x.issubset(user_liked_movies))]
                rules = set(matching_rules["consequents"].explode().unique())
                self.recommendations[self.current_cluster][user_id].update(rules)
                self.new_recommendations[user_id].update(
                    self.recommendations[self.current_cluster][user_id].difference(user_liked_movies))
        elif cluster_strategy == "grouped":
            rules = set(self.rules["consequents"].explode().unique())
            self.recommendations[self.current_cluster] = {user: rules for user in self.users["user"].unique()}
            self.new_recommendations = {user: recs.difference(self.liked_movies[user]) for user, recs in
                                        self.recommendations[self.current_cluster].items()}


def initialize_recommender():
    K = 4
    ratings = pd.DataFrame(Rating.objects.all().values("movie", "user", "value"))
    recommender = Recommender(ratings, K)
    recommender.create_clusters(users_info["labels_kmeans"])
    for i in range(1, K+1):
        recommender.update_current_cluster(i)
        if i == 1:
            recommender.generate_freq_items("apriori", 0.95)
            recommender.generate_rules(0.9)
        else:
            recommender.generate_freq_items("apriori", 0.15)
            recommender.generate_rules(0.9)
        recommender.generate_recs("grouped")
