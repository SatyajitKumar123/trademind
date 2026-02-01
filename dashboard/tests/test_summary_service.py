from decimal import Decimal

import pytest
from django.utils import timezone

from dashboard.services.summary_service import get_dashboard_summary
from trades.models import RealizedTrade


@pytest.mark.django_db
def test_dashboard_summary_metrics():
    RealizedTrade.objects.create(
        symbol="AAPL",
        quantity=10,
        buy_price=Decimal("100"),
        sell_price=Decimal("120"),
        pnl=Decimal("200"),
        realized_at=timezone.now(),
    )

    RealizedTrade.objects.create(
        symbol="AAPL",
        quantity=5,
        buy_price=Decimal("110"),
        sell_price=Decimal("100"),
        pnl=Decimal("-50"),
        realized_at=timezone.now(),
    )

    summary = get_dashboard_summary()

    assert summary["total_trades"] == 2
    assert summary["wins"] == 1
    assert summary["losses"] == 1
    assert summary["win_rate"] == Decimal("50.00")
    assert summary["net_pnl"] == Decimal("150")
