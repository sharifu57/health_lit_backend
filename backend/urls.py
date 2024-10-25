from django.urls import path, include
from rest_framework.routers import DefaultRouter

from backend.views import *


router = DefaultRouter()
router.register(r"", UserRegisterViewSet, basename="register")

urlpatterns = [
    path("", include(router.urls)),
    path("login/", LoginAPIView.as_view(), name="login")
]