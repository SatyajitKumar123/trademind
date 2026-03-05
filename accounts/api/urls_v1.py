from django.urls import path

from .views import (
    LoginView,
    LogoutView,
    RefreshView,
    RegisterView,
    UserProfileView,
)

app_name = "accounts_api"

urlpatterns = [
    # Authentication
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("refresh/", RefreshView.as_view(), name="refresh"),
    # User profile
    path("profile/", UserProfileView.as_view(), name="profile"),
]
