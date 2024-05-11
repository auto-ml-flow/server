from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from experiment.api.serializers import ExperimentSerializer
from experiment.models import ExperimentModel


class ExperimentViewSet(viewsets.ModelViewSet):
    queryset = ExperimentModel.objects.all()
    serializer_class = ExperimentSerializer
    permission_classes = (AllowAny,)
