from rest_framework.routers import SimpleRouter

from system.api.views import (
    CPUStatsViewSet,
    DiskStatsViewSet,
    MemoryStatsViewSet,
    NetworkStatsViewSet,
    SystemViewSet,
)

router = SimpleRouter()

router.register(r"systems", SystemViewSet, "systems")
router.register(r"network-stats", NetworkStatsViewSet, "network-stats")
router.register(r"disk-stats", DiskStatsViewSet, "disk-stats")
router.register(r"memory-stats", MemoryStatsViewSet, "memory-stats")
router.register(r"cpu-stats", CPUStatsViewSet, "cpu-stats")

urlpatterns = router.urls
