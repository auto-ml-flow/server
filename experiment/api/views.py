from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins

from core.viewsets import GenericViewSet
from experiment.api.serializers import (
    ExperimentSerializer,
    RunMetricSerializer,
    RunParamSerializer,
    RunResultSerializer,
    RunSerializer,
)
from experiment.models import (
    ExperimentModel,
    RunMetricModel,
    RunModel,
    RunParamModel,
    RunResultModel,
)


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


class RunParamViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet
):
    queryset = RunParamModel.objects.all()
    serializer_class = RunParamSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["run", "created_at"]


class RunResultViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet
):
    queryset = RunResultModel.objects.all()
    serializer_class = RunResultSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["run", "created_at"]
