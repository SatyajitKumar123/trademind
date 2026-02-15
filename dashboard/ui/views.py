from io import TextIOWrapper

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from dashboard.services.equity_curve_service import get_equity_curve
from dashboard.services.risk_metrics_service import calculate_risk_metrics
from dashboard.services.summary_service import get_dashboard_summary
from trades.adapters.registry import list_supported_brokers
from trades.models import UploadedTradeFile
from trades.services.file_hashing import compute_file_hash
from trades.services.ingestion_service import ingest_tradebook


@login_required
@require_http_methods(["GET", "POST"])
def upload_trades_view(request):
    if request.method == "POST":
        csv_file = request.FILES.get("file")
        broker = request.POST.get("broker")

        if not csv_file or not broker:
            messages.error(request, "CSV file and broker are required.")
            return redirect("dashboard-upload")

        # ---- Compute content hash ----
        file_hash = compute_file_hash(csv_file)

        # ---- Check for duplicate upload ----
        try:
            UploadedTradeFile.objects.create(
                user=request.user,
                original_name=csv_file.name,
                file_hash=file_hash,
            )
        except IntegrityError:
            messages.warning(
                request,
                "This file was already uploaded earlier. Duplicate ingestion prevented.",
            )
            return redirect("dashboard-home")

        # ---- Ingestion ----
        try:
            text_file = TextIOWrapper(csv_file.file, encoding="utf-8")
            realized_count = ingest_tradebook(
                user=request.user,
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


@login_required
def dashboard_home_view(request):
    return render(
        request,
        "dashboard/home.html",
        {
            "summary": get_dashboard_summary(request.user),
            "risk": calculate_risk_metrics(request.user),
        },
    )


@login_required
def equity_curve_view(request):
    curve = get_equity_curve(request.user)

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


@login_required
def risk_metrics_view(request):
    return render(
        request,
        "dashboard/risk_metrics.html",
        {
            "risk": calculate_risk_metrics(request.user),
        },
    )
