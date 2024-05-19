from django.db.models import Avg, Sum

from experiment.models import RunModel
from system.models import (
    CPUStatsModel,
    DiskStatsModel,
    MemoryStatsModel,
    NetworkStatsModel,
)


def get_successful_run_stats():
    successful_runs = RunModel.objects.filter(status=RunModel.DONE)
    run_stats = []

    for run in successful_runs:
        system = run.systemmodel
        memory_stats = MemoryStatsModel.objects.filter(system=system).aggregate(
            avg_usage_megabytes=Avg("usage_megabytes"), avg_usage_percentage=Avg("usage_percentage")
        )
        cpu_stats = CPUStatsModel.objects.filter(system=system).aggregate(
            avg_utilization=Avg("utilization")
        )
        disk_stats = DiskStatsModel.objects.filter(system=system).aggregate(
            avg_usage_percentage=Avg("usage_percentage"),
            avg_usage_megabytes=Avg("usage_megabytes"),
            avg_available=Avg("available"),
        )
        network_stats = NetworkStatsModel.objects.filter(system=system).aggregate(
            sum_receive_megabytes=Sum("receive_megabytes"),
            sum_transmit_megabytes=Sum("transmit_megabytes"),
        )

        run_stat = {  # maybe DTO?
            "system_ram": system.ram,
            "system_swap": system.swap,
            "system_swap_available": system.swap_available,
            "system_load_avg_last_min": system.load_avg_last_min,
            "system_load_avg_last_5_min": system.load_avg_last_5_min,
            "system_load_avg_last_15_min": system.load_avg_last_15_min,
            "dataset_n_features": run.dataset.n_features,
            "dataset_n_samples": run.dataset.n_samples,
            "avg_memory_usage_megabytes": memory_stats["avg_usage_megabytes"],
            "avg_memory_usage_percentage": memory_stats["avg_usage_percentage"],
            "avg_cpu_utilization": cpu_stats["avg_utilization"],
            "avg_disk_usage_percentage": disk_stats["avg_usage_percentage"],
            "avg_disk_usage_megabytes": disk_stats["avg_usage_megabytes"],
            "avg_disk_available": disk_stats["avg_available"],
            "sum_network_receive_megabytes": network_stats["sum_receive_megabytes"],
            "sum_network_transmit_megabytes": network_stats["sum_transmit_megabytes"],
            "duration": run.duration,
        }

        run_stats.append(run_stat)

    return run_stats
