from rest_framework import mixins

from core.viewsets import GenericViewSet
from dataset.api.serializers import DatasetSerializer
from dataset.models import DatasetModel
from rest_framework.parsers import MultiPartParser, JSONParser


class DatasetViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet
):  
    parser_classes = (MultiPartParser, JSONParser)
    serializer_class = DatasetSerializer
    queryset = DatasetModel.objects.all()
