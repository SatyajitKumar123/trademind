from django.db import transaction

from trades.models import RealizedTrade, Trade


def ingest_tradebook(
    *,
    user,
    file,
    broker: str,
) -> int:
    """
    Ingests a broker tradebook CSV and performs full analysis.

    This operation is idempotent:
    previous trades and analytics are cleared before ingest.
    """

    from trades.adapters.registry import get_adapter
    from trades.domain.trade_dto import TradeDTO
    from trades.services.analyze_trades import analyze_trades

    adapter = get_adapter(broker)
    reader = adapter.get_reader(file)

    trade_dtos: list[TradeDTO] = []

    for row in reader:
        dto = adapter.normalize(row)
        trade_dtos.append(dto)

    with transaction.atomic():
        Trade.objects.filter(user=user).delete()
        RealizedTrade.objects.filter(user=user).delete()

        Trade.objects.bulk_create(
            [
                Trade(
                    user=user,
                    symbol=t.symbol,
                    side=t.side,
                    quantity=t.quantity,
                    price=t.price,
                    executed_at=t.executed_at,
                )
                for t in trade_dtos
            ]
        )
        return analyze_trades(trade_dtos, user=user)
