from django.urls import path

from meta_algo import views

app_name = "meta_algo"
urlpatterns = [
    path("meta-algos/models", views.ModelListView.as_view(), name="list"),
]
