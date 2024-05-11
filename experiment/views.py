from django.views import generic

from experiment.models import ExperimentModel


class ExperimentListView(generic.ListView):
    template_name = "experiment/list.html"
    queryset = ExperimentModel.objects.order_by("-created_at")
    paginate_by = 10
    context_object_name = "experiments"


class ExperimentDetailView(generic.DetailView):
    template_name = "experiment/detail.html"
    model = ExperimentModel
    context_object_name = "experiment"
