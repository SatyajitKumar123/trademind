from django.urls import include, path

from trades.api.views import TradeUploadAPI, UploadJobDetailAPI

urlpatterns = [
    path("trades/", include("trades.api.urls")),
    path("dashboard/", include("dashboard.api.urls")),
    path("trades/upload/", TradeUploadAPI.as_view(), name="trade-upload"),
    path("jobs/<int:job_id>/", UploadJobDetailAPI.as_view(), name="upload-job-detail"),
]
