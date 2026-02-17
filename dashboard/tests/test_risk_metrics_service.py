from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone

from dashboard.services.risk_metrics_service import calculate_risk_metrics
from trades.models import RealizedTrade

User = get_user_model()


@pytest.mark.django_db
def test_calculate_risk_metrics():
    user = User.objects.create_user(username="testuser", password="pass")

    RealizedTrade.objects.create(
        user=user,
        symbol="AAPL",
        quantity=10,
        buy_price=Decimal("100"),
        sell_price=Decimal("120"),
        pnl=Decimal("200"),
        realized_at=timezone.now(),
    )

    RealizedTrade.objects.create(
        user=user,
        symbol="AAPL",
        quantity=5,
        buy_price=Decimal("110"),
        sell_price=Decimal("100"),
        pnl=Decimal("-50"),
        realized_at=timezone.now(),
    )

    metrics = calculate_risk_metrics(user=user)

    assert metrics["max_drawdown"] == Decimal("50.00")
    assert metrics["profit_factor"] == Decimal("4.00")
    assert metrics["risk_reward_ratio"] == Decimal("4.00")
    assert metrics["largest_win"] == Decimal("200.00")
    assert metrics["largest_loss"] == Decimal("-50.00")
