from dataclasses import dataclass
from decimal import Decimal


@dataclass
class PositionLot:
    symbol: str
    quantity: int
    price: Decimal
