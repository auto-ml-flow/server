from django.contrib import admin

from meta_algo.models import MetaAlgoModel, PreparedDatasetModel

admin.site.register(MetaAlgoModel)
admin.site.register(PreparedDatasetModel)
