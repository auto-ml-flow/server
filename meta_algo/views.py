from django.views import generic

from meta_algo.models import MetaAlgoModel


class ModelListView(generic.ListView):
    template_name = "models/list.html"
    queryset = MetaAlgoModel.objects.order_by("-created_at")
    context_object_name = "models"
