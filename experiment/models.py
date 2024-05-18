from django.db import models

from core.models import BaseModel


class ExperimentModel(BaseModel):
    name = models.CharField(max_length=500, unique=True)
    description = models.TextField(null=True, blank=True)


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
    description = models.TextField(blank=True, null=True)
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


class RunResultModel(BaseModel):
    key = models.CharField(max_length=100)
    value = models.FloatField()
    run = models.ForeignKey(to=RunModel, on_delete=models.CASCADE, related_name="results")


class RunParamModel(BaseModel):
    key = models.CharField(max_length=100)
    value = models.CharField()
    run = models.ForeignKey(to=RunModel, on_delete=models.CASCADE, related_name="params")
