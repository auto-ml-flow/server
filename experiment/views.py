from typing import Any

from django.http import HttpRequest, HttpResponse
from django.views import generic

from experiment.models import ExperimentModel, RunModel
from django.shortcuts import render
from django.db.models import Count

from system.models import CPUStatsModel, MemoryStatsModel, NetworkStatsModel, SystemModel
from django.db.models import Avg, Sum

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


def index_view(request) -> HttpResponse:
    # Number of unique systems
    unique_systems_count = SystemModel.objects.values('cpu_name', 'gpu_name', 'ram').distinct().count()

    # Most popular system
    most_popular_system = (
        SystemModel.objects.values('cpu_name', 'gpu_name', 'ram')
        .annotate(count=Count('id'))
        .order_by('-count')
        .first()
    )

    # Longest run
    longest_run = RunModel.objects.order_by('-duration').first()

    # Average CPU utilization
    avg_cpu_utilization = CPUStatsModel.objects.aggregate(avg_utilization=Avg('utilization'))['avg_utilization']

    # System with highest memory usage
    highest_memory_usage_system = (
        MemoryStatsModel.objects.order_by('-usage_megabytes')
        .select_related('system')
        .first()
    )
    if highest_memory_usage_system:
        highest_memory_usage_system.system

    # Total network traffic
    total_network_traffic = NetworkStatsModel.objects.aggregate(
        total_receive=Sum('receive_megabytes'),
        total_transmit=Sum('transmit_megabytes'),
    )

    context = {
        'unique_systems_count': unique_systems_count,
        'most_popular_system': most_popular_system,
        'longest_run': longest_run,
        'avg_cpu_utilization': avg_cpu_utilization,
        'highest_memory_usage_system': highest_memory_usage_system,
        'total_network_traffic': total_network_traffic,
    }
    return render(request, 'index.html', context)