from decimal import Decimal

from django.db.models import Avg

from trades.models import RealizedTrade


def get_performance_metrics() -> dict:
    """
    Returns core trading performance metrics derived from realized trades.
    """

    total_trades = RealizedTrade.objects.count()

    if total_trades == 0:
        return {
            "total_trades": 0,
            "win_rate": Decimal("0"),
            "loss_rate": Decimal("0"),
            "avg_win": Decimal("0"),
            "avg_loss": Decimal("0"),
            "expectancy": Decimal("0"),
        }

    winning_trades = RealizedTrade.objects.filter(pnl__gt=0)
    losing_trades = RealizedTrade.objects.filter(pnl__lt=0)

    win_count = winning_trades.count()
    loss_count = losing_trades.count()

    win_rate = Decimal(win_count * 100) / Decimal(total_trades)
    loss_rate = Decimal(loss_count * 100) / Decimal(total_trades)

    avg_win = winning_trades.aggregate(avg=Avg("pnl"))["avg"] or Decimal("0")
    avg_loss = losing_trades.aggregate(avg=Avg("pnl"))["avg"] or Decimal("0")

    # Expectancy formula
    expectancy = (win_rate / 100 * avg_win) + (loss_rate / 100 * avg_loss)

    return {
        "total_trades": total_trades,
        "win_rate": win_rate.quantize(Decimal("0.01")),
        "loss_rate": loss_rate.quantize(Decimal("0.01")),
        "avg_win": avg_win.quantize(Decimal("0.01")),
        "avg_loss": abs(avg_loss.quantize(Decimal("0.01"))),
        "expectancy": expectancy.quantize(Decimal("0.01")),
    }
