from django.apps import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler

global recommender


def start(recommender_instance):
    from movies.recommender_app import generate_recs
    scheduler = BackgroundScheduler()
    scheduler.add_job(generate_recs, 'interval', args=[recommender_instance, True], minutes=5)
    scheduler.start()


class RecommenderConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "recommender"

    def ready(self):
        from movies.recommender_app import generate_recs  # refresh_clusters
        global recommender
        recommender = 1 #generate_recs()
    #     start(recommender)
