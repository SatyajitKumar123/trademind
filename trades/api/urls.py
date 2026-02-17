from django.urls import path

from .views import TradeUploadAPI

urlpatterns = [
    path("upload/", TradeUploadAPI.as_view(), name="trade-upload"),
]
