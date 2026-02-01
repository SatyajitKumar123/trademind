from django.urls import path

from dashboard.api.views import (
    dashboard_summary_view,
    equity_curve_view,
    risk_metrics_view,
)

urlpatterns = [
    path("summary/", dashboard_summary_view, name="dashboard-summary"),
    path("equity-curve/", equity_curve_view, name="equity-curve"),
    path("risk-metrics/", risk_metrics_view, name="risk-metrics"),
]
