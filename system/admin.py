from django.contrib import admin

from system.models import CPUStatsModel, DiskStatsModel, NetworkStatsModel, SystemModel

admin.site.register(SystemModel)
admin.site.register(CPUStatsModel)
admin.site.register(NetworkStatsModel)
admin.site.register(DiskStatsModel)
