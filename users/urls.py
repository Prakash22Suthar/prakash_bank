from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from .views import UserViewset, LoginTokenGenerateView

app_name = "user"

router = DefaultRouter()

router.register("user", UserViewset, basename= "user")


urlpatterns = [
    path("", include(router.urls)),
    path("login", LoginTokenGenerateView.as_view(), name="login"),
    path("refresh", TokenRefreshView.as_view(), name="refresh_token"),
    path("verify-token", TokenVerifyView.as_view(), name="token_verify")
]