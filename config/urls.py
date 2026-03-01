from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from accounts.views import profile_view, register_view

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    # Web Authentication (Session-based for UI)
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="accounts/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", register_view, name="register"),
    path("profile/", profile_view, name="profile"),
    # Application Routes (UI)
    path("dashboard/", include("dashboard.urls")),
    # API Routes - ALL UNDER VERSIONING
    path("api/v1/", include("config.api_v1_urls")),
    # API Schema & Docs (keep these at root, they're not versioned)
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
