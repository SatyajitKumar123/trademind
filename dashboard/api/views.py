from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from dashboard.services.equity_curve_service import get_equity_curve
from dashboard.services.risk_metrics_service import calculate_risk_metrics
from dashboard.services.summary_service import get_dashboard_summary


class DashboardSummaryAPI(APIView):
    def get(self, request):
        data = get_dashboard_summary()

        if not data:
            return Response(
                {"detail": "No summary data available"},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(data, status=status.HTTP_200_OK)


class EquityCurveAPI(APIView):
    def get(self, request):
        data = get_equity_curve()

        if not data:
            return Response(
                {"detail": "No equity curve data available"},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(data, status=status.HTTP_200_OK)


class RiskMetricsAPI(APIView):
    def get(self, request):
        data = calculate_risk_metrics()

        if not data:
            return Response(
                {"detail": "No risk metrics available"},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(data, status=status.HTTP_200_OK)
