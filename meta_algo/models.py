from django.db import models

from core.models import BaseModel


class PreparedDatasetModel(BaseModel):
    labels = models.JSONField()
    target = models.CharField(max_length=100)
    csv_file = models.FileField(upload_to="prepared_datasets")


class MetaAlgoModel(BaseModel):
    DURATION = "DURATION"
    PREDICT = "PREDICT"

    TYPE = {
        DURATION: "DURATION",
        PREDICT: "PREDICT",
    }

    type = models.CharField(
        max_length=8,
        choices=TYPE,
        default=DURATION,
    )
    model = models.FileField(upload_to="meta_algos")
    mse = models.FloatField()
    rmse = models.FloatField()
    max_error = models.FloatField()
    min_error = models.FloatField()
    dataset = models.ForeignKey(
        to=PreparedDatasetModel, on_delete=models.CASCADE, null=True, related_name="models"
    )
