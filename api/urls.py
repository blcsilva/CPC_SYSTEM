from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, CampaignViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'campaigns', CampaignViewSet)

urlpatterns = router.urls
