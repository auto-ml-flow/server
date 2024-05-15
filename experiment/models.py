from django.db import models

from core.models import BaseModel


class ExperimentModel(BaseModel):
    name = models.CharField(max_length=200)


class RunModel(BaseModel):
    CREATED = "CREATED"
    STARTED = "STARTED"
    FAILED = "FAILED"
    DONE = "DONE"

    STATUS = {
        CREATED: "CREATED",
        STARTED: "STARTED",
        FAILED: "FAILED",
        DONE: "DONE",
    }
    experiment = models.ForeignKey(
        to=ExperimentModel, on_delete=models.CASCADE, related_name="runs"
    )
    duration = models.FloatField(blank=True, default=0)
    status = models.CharField(
        max_length=7,
        choices=STATUS,
        default=CREATED,
    )
    traceback = models.TextField(null=True, blank=True)


class RunMetricModel(BaseModel):
    key = models.CharField(max_length=100)
    value = models.FloatField()
    run = models.ForeignKey(to=RunModel, on_delete=models.CASCADE, related_name="metrics")
