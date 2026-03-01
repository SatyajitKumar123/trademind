from django.urls import path

from .views import TradeUploadAPI, UploadJobDetailAPI, UploadJobListAPI

urlpatterns = [
    path("upload/", TradeUploadAPI.as_view(), name="trade-upload"),
    path("jobs/", UploadJobListAPI.as_view(), name="upload-job-list"),
    path("jobs/<int:job_id>/", UploadJobDetailAPI.as_view(), name="upload-job-detail"),
]
