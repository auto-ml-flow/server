from rest_framework.routers import SimpleRouter

from experiment.api.views import ExperimentViewSet

router = SimpleRouter()

router.register("experiments", ExperimentViewSet, "experiments")

urlpatterns = router.urls
