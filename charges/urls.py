from rest_framework.routers import DefaultRouter

from charges.views import GenerateTokenViewSet

router = DefaultRouter()
router.register('', GenerateTokenViewSet, basename='transferData')

urlpatterns = router.urls
