from decimal import Decimal

from django.db import models
from django.utils import timezone


class Trade(models.Model):
    class Side(models.TextChoices):
        BUY = "BUY", "Buy"
        SELL = "SELL", "Sell"

    symbol = models.CharField(max_length=20)
    side = models.CharField(max_length=4, choices=Side.choices)

    quantity = models.PositiveIntegerField()
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Execution price per unit",
    )

    executed_at = models.DateTimeField(
        help_text="Actual trade execution time (exchange time)"
    )
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        indexes = [
            models.Index(fields=["symbol"]),
            models.Index(fields=["executed_at"]),
        ]
        ordering = ["executed_at"]

    def __str__(self) -> str:
        return f"{self.symbol} | {self.side} | {self.quantity} @ {self.price}"

    @property
    def trade_value(self) -> Decimal:
        """
        Total notational value of the trade.
        """
        return self.price * self.quantity
