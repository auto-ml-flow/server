from django.urls import path

from experiment import views

app_name = "experiments"
urlpatterns = [
    path("", views.ExperimentListView.as_view(), name="list"),
    path("<int:pk>/", views.ExperimentDetailView.as_view(), name="detail"),
]
