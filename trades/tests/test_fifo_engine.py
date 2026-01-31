from datetime import datetime
from decimal import Decimal

from trades.domain.fifo_engine import FIFOMatchingEngine
from trades.domain.trade_dto import TradeDTO


def test_fifo_partial_and_full_match():
    engine = FIFOMatchingEngine()

    trades = [
        TradeDTO("AAPL", "BUY", 10, Decimal("100"), datetime.now()),
        TradeDTO("AAPL", "BUY", 5, Decimal("110"), datetime.now()),
        TradeDTO("AAPL", "SELL", 12, Decimal("120"), datetime.now()),
    ]

    result = engine.process(trades)

    assert len(result) == 2
    assert result[0].pnl == Decimal("200")  # (120 - 100) * 10
    assert result[1].pnl == Decimal("20")  # (120 - 110) * 2
