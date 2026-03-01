from django.urls import include, path

urlpatterns = [
    path("trades/", include("trades.api.urls_v1")),
    path("dashboard/", include("dashboard.api.urls_v1")),
    path("auth/", include("accounts.api.urls_v1")),
]
