from decimal import Decimal

from django.db import models

from trades.models import RealizedTrade


def get_dashboard_summary() -> dict:
    trades = RealizedTrade.objects.all()

    total_trades = trades.count()

    if total_trades == 0:
        return {
            "total_trades": 0,
            "wins": 0,
            "losses": 0,
            "win_rate": Decimal("0"),
            "loss_rate": Decimal("0"),
            "net_pnl": Decimal("0"),
            "avg_win": Decimal("0"),
            "avg_loss": Decimal("0"),
            "expectancy": Decimal("0"),
        }

    wins = trades.filter(pnl__gt=0)
    losses = trades.filter(pnl__lt=0)

    win_count = wins.count()
    loss_count = losses.count()

    net_pnl = trades.aggregate(total=models.Sum("pnl"))["total"] or Decimal("0")

    avg_win = wins.aggregate(avg=models.Avg("pnl"))["avg"] or Decimal("0")
    avg_loss = losses.aggregate(avg=models.Avg("pnl"))["avg"] or Decimal("0")

    win_rate = (Decimal(win_count) / Decimal(total_trades)) * Decimal("100")
    loss_rate = Decimal("100") - win_rate

    expectancy = (win_rate / Decimal("100")) * avg_win + (
        loss_rate / Decimal("100")
    ) * avg_loss

    return {
        "total_trades": total_trades,
        "wins": win_count,
        "losses": loss_count,
        "win_rate": win_rate.quantize(Decimal("0.01")),
        "loss_rate": loss_rate.quantize(Decimal("0.01")),
        "net_pnl": net_pnl,
        "avg_win": avg_win,
        "avg_loss": avg_loss,
        "expectancy": expectancy.quantize(Decimal("0.01")),
    }
