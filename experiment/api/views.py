from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins

from core.viewsets import GenericViewSet
from experiment.api.serializers import (
    ExperimentSerializer,
    RunMetricSerializer,
    RunSerializer,
)
from experiment.models import ExperimentModel, RunMetricModel, RunModel


class ExperimentViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet
):
    queryset = ExperimentModel.objects.all()
    serializer_class = ExperimentSerializer
    lookup_field = "name"


class RunViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset = RunModel.objects.all()
    serializer_class = RunSerializer


class RunMetricViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet
):
    queryset = RunMetricModel.objects.all()
    serializer_class = RunMetricSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["run", "created_at"]
