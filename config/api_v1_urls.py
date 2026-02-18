from django.urls import include, path

urlpatterns = [
    path("trades/", include("trades.api.urls")),
    path("dashboard/", include("dashboard.api.urls")),
]
