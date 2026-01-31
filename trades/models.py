from decimal import Decimal

from django.db import models


class Trade(models.Model):
    class Side(models.TextChoices):
        BUY = "BUY"
        SELL = "SELL"

    symbol = models.CharField(max_length=50)
    side = models.CharField(max_length=4, choices=Side.choices)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=4)
    executed_at = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.symbol} {self.side} {self.quantity} @ {self.price}"

    @property
    def trade_value(self) -> Decimal:
        """
        Total notional value of the trade.
        BUY or SELL does not matter here.
        """
        return self.price * Decimal(self.quantity)


class RealizedTrade(models.Model):
    symbol = models.CharField(max_length=50)

    quantity = models.PositiveIntegerField()

    buy_price = models.DecimalField(max_digits=12, decimal_places=4)
    sell_price = models.DecimalField(max_digits=12, decimal_places=4)

    pnl = models.DecimalField(max_digits=14, decimal_places=4)

    realized_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.symbol} PnL {self.pnl}"
