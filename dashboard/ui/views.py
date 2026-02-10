from io import TextIOWrapper

from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from dashboard.services.equity_curve_service import get_equity_curve
from dashboard.services.risk_metrics_service import calculate_risk_metrics
from dashboard.services.summary_service import get_dashboard_summary
from trades.adapters.registry import list_supported_brokers
from trades.services.ingestion_service import ingest_tradebook


@require_http_methods(["GET", "POST"])
def upload_trades_view(request):
    if request.method == "POST":
        csv_file = request.FILES.get("file")
        broker = request.POST.get("broker")

        if not csv_file or not broker:
            messages.error(request, "CSV file and broker are required.")
            return redirect("dashboard-upload")

        try:
            text_file = TextIOWrapper(csv_file.file, encoding="utf-8")
            realized_count = ingest_tradebook(
                file=text_file,
                broker=broker,
            )
            messages.success(
                request,
                f"Tradebook ingested successfully. "
                f"{realized_count} realized trades created.",
            )
            return redirect("dashboard-home")

        except Exception as exc:
            messages.error(request, str(exc))
            return redirect("dashboard-upload")

    return render(
        request,
        "dashboard/upload.html",
        {
            "brokers": list_supported_brokers(),
        },
    )


def dashboard_home_view(request):
    return render(
        request,
        "dashboard/home.html",
        {
            "summary": get_dashboard_summary(),
            "risk": calculate_risk_metrics(),
        },
    )


def equity_curve_view(request):
    curve = get_equity_curve()

    context = {
        "curve": [
            {
                "timestamp": p["timestamp"].isoformat(),
                "equity": float(p["equity"]),
            }
            for p in curve
        ]
    }
    return render(request, "dashboard/equity_curve.html", context)


def risk_metrics_view(request):
    return render(
        request,
        "dashboard/risk_metrics.html",
        {
            "risk": calculate_risk_metrics(),
        },
    )
