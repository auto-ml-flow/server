from django.urls import path

from dataset import views

app_name = "datasets"
urlpatterns = [
    path("datasets/", views.DatasetListView.as_view(), name="list"),
    path("datasets/<int:pk>", views.DatasetDetailView.as_view(), name="detail"),
]
