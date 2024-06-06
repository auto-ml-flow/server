from rest_framework.routers import SimpleRouter

from meta_algo.api.views import MetaAlgoViewSet

router = SimpleRouter()

router.register("meta-algos", MetaAlgoViewSet)

urlpatterns = router.urls
