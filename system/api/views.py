from rest_framework import mixins

from core.viewsets import GenericViewSet
from system.api.serializers import (
    CPUStatsSerializer,
    DiskStatsSerializer,
    MemoryStatsSerializer,
    NetworkStatsSerializer,
    SystemSerializer,
)
from system.models import (
    CPUStatsModel,
    DiskStatsModel,
    MemoryStatsModel,
    NetworkStatsModel,
    SystemModel,
)


class SystemViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet
):
    serializer_class = SystemSerializer
    queryset = SystemModel.objects.all()


class NetworkStatsViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet
):
    serializer_class = NetworkStatsSerializer
    queryset = NetworkStatsModel.objects.all()


class DiskStatsViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet
):
    serializer_class = DiskStatsSerializer
    queryset = DiskStatsModel.objects.all()


class MemoryStatsViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet
):
    serializer_class = MemoryStatsSerializer
    queryset = MemoryStatsModel.objects.all()


class CPUStatsViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet
):
    serializer_class = CPUStatsSerializer
    queryset = CPUStatsModel.objects.all()
