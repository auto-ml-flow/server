from django.urls import path

from experiment import views

app_name = "experiments"
urlpatterns = [
    path("", views.index_view, name="index"),
    path("experiments/", views.ExperimentListView.as_view(), name="list"),
    path("experiments/<int:pk>/", views.ExperimentDetailView.as_view(), name="detail"),
    path("runs/<int:pk>/", views.RunDetailView.as_view(), name="run-detail"),
]
