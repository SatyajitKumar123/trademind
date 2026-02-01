from django.urls import path

from dashboard.api.views import dashboard_summary_view, equity_curve_view

urlpatterns = [
    path("summary/", dashboard_summary_view, name="dashboard-summary"),
    path("equity-curve/", equity_curve_view, name="equity-curve"),
]
