from rest_framework.routers import DefaultRouter

from donation.views import DonationViewSet

router = DefaultRouter()
router.register('', DonationViewSet, basename='donation')

urlpatterns = router.urls
