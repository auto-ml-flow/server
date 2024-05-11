from rest_framework import serializers

from experiment.models import ExperimentModel


class ExperimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperimentModel
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")
