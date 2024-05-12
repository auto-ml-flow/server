from rest_framework import serializers

from system.models import (
    CPUStatsModel,
    DiskStatsModel,
    MemoryStatsModel,
    NetworkStatsModel,
    SystemModel,
)


class SystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemModel
        fields = "__all__"
        read_only_fields = ("updated_at",)


class NetworkStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkStatsModel
        fields = "__all__"
        read_only_fields = ("updated_at",)


class CPUStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CPUStatsModel
        fields = "__all__"
        read_only_fields = ("updated_at",)


class MemoryStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemoryStatsModel
        fields = "__all__"
        read_only_fields = ("updated_at",)


class DiskStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiskStatsModel
        fields = "__all__"
        read_only_fields = ("updated_at",)
