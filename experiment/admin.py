from django.contrib import admin

from experiment.models import ExperimentModel, RunMetricModel, RunModel

admin.site.register(ExperimentModel)
admin.site.register(RunModel)
admin.site.register(RunMetricModel)
