from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel
from experiment.models import RunModel


class MemoryStatsModel(BaseModel):
    usage_megabytes = models.FloatField(verbose_name=_("System memory usage megabytes"))
    usage_percentage = models.FloatField(verbose_name=_("System memory usage percentage"))
    system = models.ForeignKey(
        to="SystemModel",
        on_delete=models.CASCADE,
        related_name="system_statistics",
    )


class CPUStatsModel(BaseModel):
    utilization = models.FloatField(verbose_name=_("CPU utilization percentage"))
    system = models.ForeignKey(
        to="SystemModel",
        on_delete=models.CASCADE,
        related_name="cpu_statistics",
    )


class DiskStatsModel(BaseModel):
    usage_percentage = models.FloatField(verbose_name=_("Disk usage percentage"))
    usage_megabytes = models.FloatField(verbose_name=_("Disk usage megabytes"))
    available = models.FloatField(verbose_name=_("Available disk space"))
    system = models.ForeignKey(
        to="SystemModel",
        on_delete=models.CASCADE,
        related_name="disk_statistics",
    )


class NetworkStatsModel(BaseModel):
    receive_megabytes = models.FloatField(verbose_name=_("Network recieved megabytes"))
    transmit_megabytes = models.FloatField(verbose_name=_("Network transmitted megabytes"))
    system = models.ForeignKey(
        to="SystemModel",
        on_delete=models.CASCADE,
        related_name="network_statistics",
    )


class SystemModel(BaseModel):
    run = models.OneToOneField(to=RunModel, on_delete=models.SET_NULL, null=True)
    name = models.CharField(
        max_length=120, blank=True, null=True, verbose_name=_("Custom setted system name")
    )
    cpu_name = models.CharField(max_length=200)
    gpu_name = models.CharField(max_length=200, blank=True, null=True)
    ram = models.BigIntegerField()
    ram_available = models.BigIntegerField()
    swap = models.BigIntegerField()
    swap_available = models.BigIntegerField()
    load_avg_last_min = models.FloatField()
    load_avg_last_5_min = models.FloatField()
    load_avg_last_15_min = models.FloatField()

    def __str__(self) -> str:
        return f"Computer with Name: {self.name} CPU: {self.cpu_name} RAM: {self.ram}"
