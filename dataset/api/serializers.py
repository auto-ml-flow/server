from rest_framework import serializers

from dataset.models import DatasetModel


class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatasetModel
        fields = "__all__"
        read_only_fields = ("updated_at",)

