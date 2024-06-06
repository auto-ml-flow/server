from rest_framework import serializers

class MetaAlgoFeaturesSerializer(serializers.Serializer):
    system_ram = serializers.IntegerField()
    system_swap = serializers.IntegerField()
    system_swap_available = serializers.IntegerField()
    system_load_avg_last_min = serializers.FloatField()
    system_load_avg_last_5_min = serializers.FloatField()
    system_load_avg_last_15_min = serializers.FloatField()
    dataset_n_features = serializers.IntegerField()
    dataset_n_samples = serializers.IntegerField()
    avg_memory_usage_megabytes = serializers.FloatField()
    avg_memory_usage_percentage = serializers.FloatField()
    avg_cpu_utilization = serializers.FloatField()
    avg_disk_usage_percentage = serializers.FloatField()
    avg_disk_usage_megabytes = serializers.FloatField()
    avg_disk_available = serializers.FloatField()
    sum_network_receive_megabytes = serializers.FloatField()
    sum_network_transmit_megabytes = serializers.FloatField()

class MetaAlgoPredictionsSerializer(serializers.Serializer):
    duration = serializers.FloatField()
