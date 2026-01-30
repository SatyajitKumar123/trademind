from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(frozen=True)
class TradeDTO:
    symbol: str
    side: str
    quantity: int
    price: Decimal
    executed_at: datetime
