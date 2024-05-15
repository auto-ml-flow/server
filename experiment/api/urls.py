from rest_framework.routers import SimpleRouter

from experiment.api.views import ExperimentViewSet, RunMetricViewSet, RunViewSet

router = SimpleRouter()

router.register("experiments", ExperimentViewSet, "experiments")
router.register("runs", RunViewSet, "runs")
router.register("run-metrics", RunMetricViewSet, "run-metrics")

urlpatterns = router.urls
