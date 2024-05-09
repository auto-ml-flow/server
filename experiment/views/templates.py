from django.views import generic

from experiment.models import ExperimentModel


class IndexView(generic.ListView):
    template_name = "experiments/index.html"
    context_object_name = "latest_experiment_list"
    queryset =  ExperimentModel.objects.order_by("-created_at")[:5]


class DetailView(generic.DetailView):
    model = ExperimentModel
    template_name = "experiments/detail.html"
    context_object_name = "experiment"
