from django.db import models

from core.models import BaseModel


class ExperimentModel(BaseModel):
    name = models.CharField(max_length=200)
