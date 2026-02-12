from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from dashboard.services.equity_curve_service import get_equity_curve
from dashboard.services.risk_metrics_service import calculate_risk_metrics
from dashboard.services.summary_service import get_dashboard_summary


@extend_schema(
    summary="Dashboard Summary",
    description="Returns overall performance summary including PnL, win rate, etc.",
)
class DashboardSummaryAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = get_dashboard_summary(request.user)
        return Response(data, status=status.HTTP_200_OK)


class EquityCurveAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = get_equity_curve(request.user)
        return Response(data, status=status.HTTP_200_OK)


class RiskMetricsAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = calculate_risk_metrics(request.user)
        return Response(data, status=status.HTTP_200_OK)
