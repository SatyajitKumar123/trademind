from datetime import datetime
from decimal import Decimal, InvalidOperation

from django.utils import timezone

from trades.adapters.base import BrokerAdapter
from trades.domain.trade_dto import TradeDTO


class ZerodhaAdapter(BrokerAdapter):
    def normalize(self, row: dict) -> TradeDTO:
        # --- Side normalization ---
        side_raw = row["trade_type"].strip().upper()
        if side_raw not in {"BUY", "SELL"}:
            raise ValueError(f"Invalid side: {row['trade_type']}")
        side = side_raw

        # --- Datetime normalization ---
        executed_at = datetime.fromisoformat(row["order_execution_time"])
        executed_at = timezone.make_aware(executed_at)

        # --- Quantity normalization (CRITICAL FIX) ---
        raw_qty = row["quantity"]
        try:
            qty_decimal = Decimal(str(raw_qty))
        except InvalidOperation as err:
            raise ValueError(f"Invalid quantity value: {raw_qty}") from err

        if qty_decimal % 1 != 0:
            raise ValueError(f"Non-integer quantity not supported: {raw_qty}")

        quantity = int(qty_decimal)

        # --- Price normalization ---
        try:
            price = Decimal(str(row["price"]))
        except InvalidOperation as err:
            raise ValueError(f"Invalid price value: {row['price']}") from err

        return TradeDTO(
            symbol=row["symbol"].strip(),
            side=side,
            quantity=quantity,
            price=price,
            executed_at=executed_at,
        )
