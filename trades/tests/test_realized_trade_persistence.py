from decimal import Decimal

import pytest

from trades.domain.realized_pnl import RealizedPnL
from trades.models import RealizedTrade
from trades.services.pnl_service import persist_realized_pnl


@pytest.mark.django_db
def test_realized_pnl_persistence():
    results = [
        RealizedPnL(
            symbol="AAPL",
            quantity=10,
            buy_price=Decimal("100"),
            sell_price=Decimal("120"),
            pnl=Decimal("200"),
        )
    ]

    count = persist_realized_pnl(results)

    assert count == 1
    assert RealizedTrade.objects.count() == 1

    record = RealizedTrade.objects.first()
    assert record.pnl == Decimal("200")
