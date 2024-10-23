from django.urls import path
from rest_framework.routers import DefaultRouter

from backend.views import UserRegisterViewSet


router = DefaultRouter()
router.register(r"", UserRegisterViewSet, basename="signUpUser")

urlpatterns = [
    # path()
]