from decimal import Decimal

from trades.models import RealizedTrade

ZERO = Decimal("0.00")


def calculate_risk_metrics() -> dict:
    """
    Computes drawdown and risk metrics from realized trades.

    Metrics:
    - max_drawdown (absolute)
    - profit_factor
    - risk_reward_ratio
    - largest_win
    - largest_loss

    All values are Decimal and normalized for API use.
    """

    qs = RealizedTrade.objects.all()

    # ---- Empty dataset guard (correct QuerySet check) ----
    if not qs.exists():
        return {
            "max_drawdown": ZERO,
            "profit_factor": ZERO,
            "risk_reward_ratio": ZERO,
            "largest_win": ZERO,
            "largest_loss": ZERO,
        }

    # ---- Ordered PnL stream (memory efficient) ----
    pnls = qs.order_by("realized_at").values_list("pnl", flat=True)

    equity = Decimal("0")
    peak = Decimal("0")
    max_drawdown = Decimal("0")

    total_profit = Decimal("0")
    total_loss = Decimal("0")

    win_count = 0
    loss_count = 0

    largest_win = Decimal("0")
    largest_loss = Decimal("0")

    # ---- Single pass over trades ----
    for pnl in pnls:
        # Equity & drawdown
        equity += pnl
        if equity > peak:
            peak = equity

        drawdown = peak - equity
        if drawdown > max_drawdown:
            max_drawdown = drawdown

        # Profit / loss tracking
        if pnl > 0:
            total_profit += pnl
            win_count += 1
            if pnl > largest_win:
                largest_win = pnl
        elif pnl < 0:
            total_loss += pnl  # negative
            loss_count += 1
            if pnl < largest_loss:
                largest_loss = pnl

    total_loss_abs = abs(total_loss)

    # ---- Profit Factor ----
    profit_factor = (
        total_profit / total_loss_abs if total_loss_abs > 0 else Decimal("0")
    )

    # ---- Risk-Reward Ration ----
    avg_win = total_profit / win_count if win_count > 0 else Decimal("0")

    avg_loss = total_loss_abs / loss_count if loss_count > 0 else Decimal("0")

    risk_reward_ratio = avg_win / avg_loss if avg_loss > 0 else Decimal("0")

    # ---- Normalized API output ----
    return {
        "max_drawdown": max_drawdown.quantize(Decimal("0.01")),
        "profit_factor": profit_factor.quantize(Decimal("0.01")),
        "risk_reward_ratio": risk_reward_ratio.quantize(Decimal("0.01")),
        "largest_win": largest_win.quantize(Decimal("0.01")),
        "largest_loss": largest_loss.quantize(Decimal("0.01")),
    }
