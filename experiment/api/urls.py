from rest_framework.routers import SimpleRouter

from experiment.api.views import (
    ExperimentViewSet,
    RunMetricViewSet,
    RunParamViewSet,
    RunResultViewSet,
    RunViewSet,
)

router = SimpleRouter()

router.register("experiments", ExperimentViewSet, "experiments")
router.register("runs", RunViewSet, "runs")
router.register("run-metrics", RunMetricViewSet, "run-metrics")
router.register("run-params", RunParamViewSet, "run-params")
router.register("run-results", RunResultViewSet, "run-results")

urlpatterns = router.urls
