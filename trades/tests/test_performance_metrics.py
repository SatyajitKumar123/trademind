from decimal import Decimal

import pytest

from trades.models import RealizedTrade
from trades.services.performance_metrics import get_performance_metrics


@pytest.mark.django_db
def test_performance_metrics_calculation():
    RealizedTrade.objects.create(
        symbol="AAPL",
        quantity=10,
        buy_price=Decimal("100"),
        sell_price=Decimal("120"),
        pnl=Decimal("200"),
    )

    RealizedTrade.objects.create(
        symbol="AAPL",
        quantity=5,
        buy_price=Decimal("110"),
        sell_price=Decimal("100"),
        pnl=Decimal("-50"),
    )

    metrics = get_performance_metrics()

    assert metrics["total_trades"] == 2
    assert metrics["win_rate"] == Decimal("50.00")
    assert metrics["loss_rate"] == Decimal("50.00")
    assert metrics["avg_win"] == Decimal("200.00")
    assert metrics["avg_loss"] == Decimal("50.00")
    assert metrics["expectancy"] == Decimal("75.00")
