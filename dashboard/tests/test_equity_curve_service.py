from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone

from dashboard.services.equity_curve_service import get_equity_curve
from trades.models import RealizedTrade

User = get_user_model()


@pytest.mark.django_db
def test_equity_curve_generation():
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

    curve = get_equity_curve(user=user)

    assert len(curve) == 2
    assert curve[0]["equity"] == Decimal("200")
    assert curve[1]["equity"] == Decimal("150")
