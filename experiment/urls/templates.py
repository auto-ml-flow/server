from django.urls import path

from experiment.views import templates

app_name = "experiments"
urlpatterns = [
    path("", templates.IndexView.as_view(), name="index"),
    path("<int:pk>/", templates.DetailView.as_view(), name="detail"),
]
