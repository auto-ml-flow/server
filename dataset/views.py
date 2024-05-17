from django.views import generic

from dataset.models import DatasetModel


class DatasetListView(generic.ListView):
    template_name = "dataset/list.html"
    model = DatasetModel
    context_object_name = "datasets"


class DatasetDetailView(generic.DetailView):
    template_name = "dataset/detail.html"
    model = DatasetModel
    context_object_name = "dataset"
