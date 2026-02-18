from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts.views import profile_view, register_view

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    # Web Authentication (Session-based)
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="accounts/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", register_view, name="register"),
    path("profile/", profile_view, name="profile"),
    # Application Routes
    path("dashboard/", include("dashboard.urls")),
    # API Routes
    path("api/", include("dashboard.api.urls")),
    path("api/trades/", include("trades.api.urls")),
    # Versioned API
    path("api/v1/", include("config.api_v1_urls")),
    # API Authentication (Token)
    path("api/token/", obtain_auth_token, name="api-token"),
    # JWT Authentication
    path("api/jwt/token/", TokenObtainPairView.as_view(), name="jwt-token"),
    path("api/jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    # API Schema & Docs
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
