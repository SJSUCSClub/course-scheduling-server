from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView
from dj_rest_auth.views import UserDetailsView
from authentication.views import GoogleLogin
from dj_rest_auth.jwt_auth import get_refresh_view

urlpatterns = [
    path("user/", UserDetailsView.as_view(), name="rest_user_details"),
    path("google/", GoogleLogin.as_view(), name="google_login"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("token/refresh/", get_refresh_view().as_view(), name="token_refresh"),
]