from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("jwt/token/", TokenObtainPairView.as_view(), name="jwt-token"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
]
