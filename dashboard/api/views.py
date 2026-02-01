from django.http import JsonResponse
from django.views.decorators.http import require_GET

from dashboard.services.equity_curve_service import get_equity_curve
from dashboard.services.risk_metrics_service import calculate_risk_metrics
from dashboard.services.summary_service import get_dashboard_summary


@require_GET
def dashboard_summary_view(request):
    data = get_dashboard_summary()
    return JsonResponse(data=data)


@require_GET
def equity_curve_view(request):
    data = get_equity_curve()
    return JsonResponse(data=data, safe=False)


@require_GET
def risk_metrics_view(request):
    data = calculate_risk_metrics()
    return JsonResponse(data=data)
