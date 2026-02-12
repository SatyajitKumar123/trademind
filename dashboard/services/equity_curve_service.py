from decimal import Decimal

from trades.models import RealizedTrade


def get_equity_curve(user) -> list[dict]:
    """
    Returns cumulative P&L over time.
    Output is frontend-chart friendly.
    """
    trades = (
        RealizedTrade.objects.filter(user=user)
        .order_by("realized_at")
        .values("realized_at", "pnl")
    )

    equity = Decimal("0")
    curve: list[dict] = []

    for trade in trades:
        equity += trade["pnl"]
        curve.append(
            {
                "timestamp": trade["realized_at"],
                "equity": equity,
            }
        )

    return curve
