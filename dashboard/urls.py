from django.urls import path

from dashboard.api.views import (
    dashboard_summary_view,
)
from dashboard.ui.views import (
    dashboard_home_view,
    equity_curve_view,
    risk_metrics_view,
    upload_trades_view,
)

urlpatterns = [
    path("summary/", dashboard_summary_view, name="dashboard-summary"),
    path("equity-curve/", equity_curve_view, name="equity-curve"),
    path("risk-metrics/", risk_metrics_view, name="risk-metrics"),
    path("ui/upload/", upload_trades_view, name="dashboard-upload"),
    path("ui/", dashboard_home_view, name="dashboard-home"),
    path("ui/equity/", equity_curve_view, name="dashboard-equity"),
    path("ui/risk/", risk_metrics_view, name="dashboard-risk"),
]
