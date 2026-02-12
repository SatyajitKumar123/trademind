from typing import Iterable

from trades.domain.realized_pnl import RealizedPnL
from trades.models import RealizedTrade


def persist_realized_pnl(results: Iterable[RealizedPnL], *, user) -> int:
    records = [
        RealizedTrade(
            user=user,
            symbol=r.symbol,
            quantity=r.quantity,
            buy_price=r.buy_price,
            sell_price=r.sell_price,
            pnl=r.pnl,
        )
        for r in results
    ]

    RealizedTrade.objects.bulk_create(records)
    return len(records)
