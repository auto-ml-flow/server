from django.db import models

from auto_ml_flow.core.models import BaseModel


class ExperimentModel(BaseModel):
    name = models.CharField(max_length=200)
