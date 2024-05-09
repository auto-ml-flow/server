from rest_framework.routers import SimpleRouter

from experiment.views.rest import ExperimentModelViewSet

router = SimpleRouter()

router.register("experiments", ExperimentModelViewSet, "experiments")

urlpatterns = router.urls
