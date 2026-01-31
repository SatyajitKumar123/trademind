from io import TextIOBase

from trades.adapters.registry import get_adapter
from trades.domain.trade_dto import TradeDTO
from trades.models import Trade
from trades.services.analyze_trades import analyze_trades


def ingest_tradebook(
    *,
    file: TextIOBase,
    broker: str,
) -> int:
    """
    Ingests a broker tradebook CSV and performs full analysis.

    Returns number of realized trades created.
    """
    adapter = get_adapter(broker)
    reader = adapter.get_reader(file)

    trade_dtos: list[TradeDTO] = []

    for row in reader:
        dto = adapter.normalize(row)
        trade_dtos.append(dto)

    # Persist raw trades
    Trade.objects.bulk_create(
        [
            Trade(
                symbol=t.symbol,
                side=t.side,
                quantity=t.quantity,
                price=t.price,
                executed_at=t.executed_at,
            )
            for t in trade_dtos
        ]
    )

    # Analyze + persist realized P&L
    return analyze_trades(trade_dtos)
