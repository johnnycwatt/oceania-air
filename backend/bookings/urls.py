from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookingViewSet, PassengerViewSet

router = DefaultRouter()
router.register(r'bookings', BookingViewSet)
router.register(r'passengers', PassengerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]