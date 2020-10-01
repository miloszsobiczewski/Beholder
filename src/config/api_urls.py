from django.urls import include, path
from rest_framework import routers

from moneyball.api import MoneyBallViewSet

router = routers.DefaultRouter()

router.register(r"moneyball", MoneyBallViewSet, basename="moneyball")

urlpatterns = [path("api/v1/", include(router.urls))]
