from django.urls import path

from system import views

app_name = "systems"
urlpatterns = [
    path("systems/", views.SystemListView.as_view(), name="list"),
    path("systems/<int:pk>/", views.system_detail_view, name="detail"),
]
