from rest_framework.routers import SimpleRouter

from dataset.api.views import DatasetViewSet

router = SimpleRouter()

router.register(r"datasets", DatasetViewSet, "datasets")

urlpatterns = router.urls
