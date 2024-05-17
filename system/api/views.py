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
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend


class SystemViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet
):
    serializer_class = SystemSerializer
    queryset = SystemModel.objects.all()

    @action(detail=True, methods=['GET'])
    def get_equal_systems(self, request: Request, pk: int, *args, **kwargs) -> Response:
        system = get_object_or_404(SystemModel, pk=pk)
        
        systems = self.queryset.filter(cpu_name=system.cpu_name, ram=system.ram)
        
        if system.gpu_name:
            systems = systems.filter(gpu_name=system.gpu_name)

        serializer = self.get_serializer(systems, many=True)
        
        return Response(serializer.data)
        
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
