from datetime import datetime
from decimal import Decimal

from django.utils import timezone

from trades.adapters.base import BrokerAdapter
from trades.domain.trade_dto import TradeDTO


class ZerodhaAdapter(BrokerAdapter):
    def normalize(self, row: dict) -> TradeDTO:
        side = row["trade_type"].strip().upper()
        if side not in {"BUY", "SELL"}:
            raise ValueError(f"Invalid side: {row['trade_type']}")

        executed_at = datetime.fromisoformat(row["order_execution_time"])
        executed_at = timezone.make_aware(executed_at)

        return TradeDTO(
            symbol=row["symbol"].strip(),
            side=side,
            quantity=int(float(row["quantity"])),  # Zerodha gives 50.000000
            price=Decimal(str(row["price"])),
            executed_at=executed_at,
        )
