import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "auto_ml_flow.settings")

app = Celery("auto_ml_flow")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "update_meta_algo": {
        "task": "meta_algo.tasks.fit_meta_algo",
        # Execute every hour
        "schedule": 3600,
    },
    "create_prepared_dataset": {
        "task": "meta_algo.tasks.create_prepared_dataset",
         # Execute every half hour
        "schedule": 1800,
    },
}
