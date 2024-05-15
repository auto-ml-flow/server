from django.views import generic

from system.models import SystemModel


class SystemListView(generic.ListView):
    template_name = "system/list.html"
    queryset = SystemModel.objects.order_by("-created_at")
    paginate_by = 10
    context_object_name = "systems"


class SystemDetailView(generic.DetailView):
    template_name = "system/detail.html"
    model = SystemModel
    context_object_name = "system"
