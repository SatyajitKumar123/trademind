from django.urls import include, path

from dashboard.ui.views import (
    dashboard_home_view,
    equity_curve_view,
    risk_metrics_view,
    upload_trades_view,
)

urlpatterns = [
    path("ui/upload/", upload_trades_view, name="dashboard-upload"),
    path("ui/", dashboard_home_view, name="dashboard-home"),
    path("ui/equity/", equity_curve_view, name="dashboard-equity"),
    path("ui/risk/", risk_metrics_view, name="dashboard-risk"),
    # API routes
    path("api/", include("dashboard.api.urls")),
]
