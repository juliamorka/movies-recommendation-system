from collections import defaultdict
from mlxtend.frequent_patterns import apriori, association_rules, fpgrowth
import pandas as pd
from .models import Rating, Recommendation, Profile, Movie
from django.contrib.auth.models import User
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from datetime import datetime

NUMBER_OF_CLUSTERS = 4


def merge_ratings_and_profiles():
    ratings = pd.DataFrame(Rating.objects.all().values("movie", "profile", "user", "value"))
    users_info = pd.DataFrame(Profile.objects.all().values("imdb_id", "cluster"))
    ratings = ratings.merge(users_info, left_on="profile", right_on="imdb_id")
    return ratings


class Recommender:
    def __init__(self):
        self.all_ratings = merge_ratings_and_profiles()
        self.ratings = self.all_ratings[self.all_ratings["value"] >= 5]
        self.profiles_users = {user_profile["profile"]: user_profile["user"] for user_profile in
                               self.ratings.to_dict("records")}
        self.current_cluster = 0
        self.frq_items, self.rules = dict(), dict()
        self.seen_movies = self.all_ratings.groupby("profile")["movie"].apply(list)
        self.new_recommendations = defaultdict(set)
        self.closest_clusters = {1: 4, 2: 4, 3: 4, 4: 2}

    def refresh_liked_movies(self):
        self.all_ratings = merge_ratings_and_profiles()
        self.ratings = self.all_ratings[self.all_ratings["value"] >= 5]
        self.seen_movies = self.all_ratings.groupby("profile")["movie"].apply(list)

    def update_current_cluster(self, cluster):
        self.current_cluster = cluster
        self.users = self.ratings[self.ratings["cluster"] == cluster]
        self.user_movie_matrix = self.users.groupby(["profile", "movie"]).sum()["value"].unstack().fillna(0).astype(
            bool)

    def generate_freq_items(self, algorithm, min_support):
        if algorithm == "apriori":
            self.frq_items[self.current_cluster] = apriori(self.user_movie_matrix, min_support=min_support,
                                                           use_colnames=True)
        elif algorithm == "fpgrowth":
            self.frq_items[self.current_cluster] = fpgrowth(self.user_movie_matrix, min_support=min_support,
                                                            use_colnames=True)

    def generate_rules(self, min_confidence):
        self.rules[self.current_cluster] = association_rules(self.frq_items[self.current_cluster], metric="confidence",
                                                             min_threshold=min_confidence)

    def generate_recs(self, cluster_strategy):
        if cluster_strategy == "grouped":
            rules = set(self.rules[self.current_cluster]["consequents"].explode().unique())
            recommendations = {user: rules for user in self.users["profile"].unique()}
            new_recommendations = {user: recs.difference(self.seen_movies[user]) for user, recs in
                                   recommendations.items()}
            for user, recs in new_recommendations.items():
                user_instance = User.objects.get(id=self.profiles_users[user])
                for movie in recs:
                    Recommendation.objects.get_or_create(user=user_instance, movie=Movie.objects.get(id=movie))


def generate_recs(recommender=None, full_clusters_refresh=False):
    # if full_clusters_refresh:
    Recommendation.objects.all().delete()
    recommender = recommender or Recommender()
    support_mapping = {1: 0.95, 2: 0.15, 3: 0.15, 4: 0.15}

    for i in range(1, NUMBER_OF_CLUSTERS + 1):
        print(i)
        recommender.update_current_cluster(i)
        recommender.generate_freq_items("fpgrowth", support_mapping[i])
        recommender.generate_rules(0.9)
        recommender.generate_recs("grouped")

    if full_clusters_refresh:
        print(f"Recs generated at {datetime.now()}")
    return recommender


# def refresh_all_clusters(recommender):
#     ratings = pd.DataFrame(Rating.objects.all().values("movie", "profile", "user", "value"))
#     ratings_grouped = ratings.groupby(by="profile")
#
#     users_info = pd.DataFrame()
#     users_info["count"] = ratings_grouped.count()["value"]
#     users_info["mean"] = ratings_grouped.mean()["value"]
#
#     scaler = MinMaxScaler((0, 1))
#
#     scaled = scaler.fit_transform(users_info)
#     users_info["count_scaled"] = scaled[:, 0]
#     users_info["mean_scaled"] = scaled[:, 1]
#
#     kmeans = KMeans(n_clusters=NUMBER_OF_CLUSTERS, random_state=0, n_init="auto")
#     kmeans.fit(users_info[["count_scaled", "mean_scaled"]])
#     users_info["labels_kmeans"] = kmeans.predict(users_info[["count_scaled", "mean_scaled"]])
#     users_info["labels_kmeans"] = users_info["labels_kmeans"] + 1
#
#     for _, row in users_info[["profile", "labels_kmeans"]].iterrows():
#         profile = Profile.objects.get(imdb_id=row["profile"])
#         profile.cluster = row["labels_kmeans"]
#         profile.save()
# centroids = kmeans.cluster_centers_
# neighbours = dict()
# for i, centroid in enumerate(centroids):
#   distances = np.sum((centroids-centroid)**2, axis=1)
#   distances[distances==0] = np.inf
#   neighbours[i+1] = np.argmin(distances)+1
#
#     recommender.closest_clusters = neighbours

#
def regenerate_recs_in_new_cluster(profile_id, recommender):
    profile = Profile.objects.get(imdb_id=profile_id)
    new_cluster = recommender.closest_clusters[profile.cluster]
    if profile.prev_cluster == new_cluster:
        return
    profile.prev_cluster = profile.cluster
    profile.cluster = new_cluster
    profile.save()
    recommender.refresh_liked_movies()
    recommender.ratings[recommender.ratings["profile"] == profile_id]["cluster"] = new_cluster
    recommender.update_current_cluster(new_cluster)
    recommender.generate_recs("grouped")
