from decimal import Decimal

from django.conf import settings
from django.db import models


class Trade(models.Model):
    class Side(models.TextChoices):
        BUY = "BUY"
        SELL = "SELL"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="trades"
    )

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
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="realized_trades",
    )

    symbol = models.CharField(max_length=50)

    quantity = models.PositiveIntegerField()

    buy_price = models.DecimalField(max_digits=12, decimal_places=4)
    sell_price = models.DecimalField(max_digits=12, decimal_places=4)

    pnl = models.DecimalField(max_digits=14, decimal_places=4)

    realized_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.symbol} PnL {self.pnl}"


class UploadedTradeFile(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="uploaded_files",
    )

    original_name = models.CharField(max_length=225)

    file_hash = models.CharField(max_length=64)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "file_hash")

    def __str__(self):
        return f"{self.original_name} ({self.user})"
