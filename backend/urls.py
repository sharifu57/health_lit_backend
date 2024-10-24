from django.urls import path
from rest_framework.routers import DefaultRouter

from backend.views import *


router = DefaultRouter()
router.register(r"", UserRegisterViewSet, basename="signUpUser")

urlpatterns = [
    # path()
    path("login/", LoginAPIView.as_view(), name="login")
]