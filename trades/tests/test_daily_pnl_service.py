from decimal import Decimal

import pytest
from django.utils import timezone

from trades.models import RealizedTrade
from trades.services.daily_pnl_service import get_daily_pnl


@pytest.mark.django_db
def test_daily_pnl_aggregation():
    now = timezone.now()

    RealizedTrade.objects.create(
        symbol="AAPL",
        quantity=10,
        buy_price=Decimal("100"),
        sell_price=Decimal("120"),
        pnl=Decimal("200"),
        realized_at=now,
    )

    RealizedTrade.objects.create(
        symbol="AAPL",
        quantity=5,
        buy_price=Decimal("110"),
        sell_price=Decimal("120"),
        pnl=Decimal("50"),
        realized_at=now,
    )

    results = get_daily_pnl(symbol="AAPL")

    assert len(results) == 1
    assert results[0]["pnl"] == Decimal("250")
