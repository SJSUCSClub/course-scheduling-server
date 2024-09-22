from django.urls import path
from . import views

urlpatterns = [
    path("authorize", views.GoogleAuthorize, name="google_login"),
    path("oauth2callback", views.oauth2callback, name="oauth2callback"),
    path("refresh", views.RefreshToken, name="refresh_tokens"),
    path("logout", views.Logout, name="logout_view"),
]
