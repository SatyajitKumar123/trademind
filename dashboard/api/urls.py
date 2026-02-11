from django.urls import path

from dashboard.api.views import (
    DashboardSummaryAPI,
    EquityCurveAPI,
    RiskMetricsAPI,
)

urlpatterns = [
    path("summary/", DashboardSummaryAPI.as_view(), name="api-dashboard-summary"),
    path("equity-curve/", EquityCurveAPI.as_view(), name="api-equity-curve"),
    path("risk-metrics/", RiskMetricsAPI.as_view(), name="api-risk-metrics"),
]
