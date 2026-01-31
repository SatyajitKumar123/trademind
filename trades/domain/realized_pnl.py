from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class RealizedPnL:
    symbol: str
    quantity: int
    buy_price: Decimal
    sell_price: Decimal
    pnl: Decimal
