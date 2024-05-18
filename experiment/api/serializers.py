from rest_framework import serializers

from experiment.models import (
    ExperimentModel,
    RunMetricModel,
    RunModel,
    RunParamModel,
    RunResultModel,
)


class ExperimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperimentModel
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")


class RunSerializer(serializers.ModelSerializer):
    class Meta:
        model = RunModel
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")


class RunMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = RunMetricModel
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")


class RunParamSerializer(serializers.ModelSerializer):
    class Meta:
        model = RunParamModel
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")


class RunResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = RunResultModel
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")
