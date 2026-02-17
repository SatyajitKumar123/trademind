from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model

from trades.models import RealizedTrade
from trades.services.performance_metrics import get_performance_metrics

User = get_user_model()


@pytest.mark.django_db
def test_performance_metrics_calculation():
    user = User.objects.create_user(username="test", password="pass")

    RealizedTrade.objects.create(
        user=user,
        symbol="AAPL",
        quantity=10,
        buy_price=Decimal("100"),
        sell_price=Decimal("120"),
        pnl=Decimal("200"),
    )

    RealizedTrade.objects.create(
        user=user,
        symbol="AAPL",
        quantity=5,
        buy_price=Decimal("110"),
        sell_price=Decimal("100"),
        pnl=Decimal("-50"),
    )

    metrics = get_performance_metrics(user=user)

    assert metrics["total_trades"] == 2
    assert metrics["win_rate"] == Decimal("50.00")
    assert metrics["loss_rate"] == Decimal("50.00")
    assert metrics["avg_win"] == Decimal("200.00")
    assert metrics["avg_loss"] == Decimal("50.00")
    assert metrics["expectancy"] == Decimal("75.00")
