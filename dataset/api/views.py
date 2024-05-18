from rest_framework import mixins
from rest_framework.parsers import JSONParser, MultiPartParser

from core.viewsets import GenericViewSet
from dataset.api.serializers import DatasetSerializer
from dataset.models import DatasetModel


class DatasetViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet
):
    parser_classes = (MultiPartParser, JSONParser)
    serializer_class = DatasetSerializer
    queryset = DatasetModel.objects.all()
