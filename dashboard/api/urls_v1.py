from django.urls import path

from .views import DashboardSummaryAPI, EquityCurveAPI, RiskMetricsAPI

urlpatterns = [
    path("summary/", DashboardSummaryAPI.as_view(), name="dashboard-summary"),
    path("equity-curve/", EquityCurveAPI.as_view(), name="equity-curve"),
    path("risk-metrics/", RiskMetricsAPI.as_view(), name="risk-metrics"),
]
