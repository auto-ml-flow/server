from core.models import BaseModel
from django.db import models

from experiment.models import RunModel


class DatasetModel(BaseModel):
    run = models.OneToOneField(to=RunModel, on_delete=models.CASCADE, related_name="dataset")
    n_samples = models.IntegerField()
    n_features = models.IntegerField()
    file = models.FileField(upload_to="datasets")
