from rest_framework import viewsets

from experiment.api.serializers import ExperimentSerializer
from experiment.models import ExperimentModel


class ExperimentViewSet(viewsets.ModelViewSet):
    queryset = ExperimentModel.objects.all()
    serializer_class = ExperimentSerializer
