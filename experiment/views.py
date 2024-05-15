from typing import Any

from django.http import HttpRequest, HttpResponse
from django.views import generic

from experiment.models import ExperimentModel, RunModel


class ExperimentListView(generic.ListView):
    template_name = "experiment/list.html"
    queryset = ExperimentModel.objects.order_by("-created_at")
    paginate_by = 15
    context_object_name = "experiments"


class ExperimentDetailView(generic.detail.SingleObjectMixin, generic.ListView):
    paginate_by = 15
    template_name = "experiment/run_detail.html"

    def get(self, request: HttpRequest, *args: list[Any], **kwargs: dict[Any, Any]) -> HttpResponse:
        self.object = self.get_object(queryset=ExperimentModel.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: dict[Any, Any]) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["experiment"] = self.object
        return context

    def get_queryset(self):  # noqa: ANN201
        return self.object.runs.all().order_by("-created_at", "id")


class RunDetailView(generic.DetailView):
    model = RunModel
    template_name = "run/detail.html"
    context_object_name = "run"
