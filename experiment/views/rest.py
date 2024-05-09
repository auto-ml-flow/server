from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from experiment.models import ExperimentModel
from experiment.serializers import ExperimentSerializer


class ExperimentModelViewSet(viewsets.ModelViewSet):
    queryset = ExperimentModel.objects.all()
    serializer_class = ExperimentSerializer
    permission_classes = (AllowAny,)
