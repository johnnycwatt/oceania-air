from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FlightViewSet, AircraftViewSet

router = DefaultRouter()
router.register(r'flights', FlightViewSet)
router.register(r'aircraft', AircraftViewSet)

urlpatterns = [
    path('', include(router.urls)),
]