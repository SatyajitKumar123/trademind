from datetime import date

from django.db.models import Sum
from django.db.models.functions import TruncDate

from trades.models import RealizedTrade


def get_daily_pnl(
    *,
    symbol: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
) -> list[dict]:
    """
    Returns daily realized P&L.

    Each item:
    {
        "date": date,
        "pnl": Decimal
    }
    """
    qs = RealizedTrade.objects.all()

    if symbol:
        qs = qs.filter(symbol=symbol)

    if start_date:
        qs = qs.filter(realized_at__date__gte=start_date)

    if end_date:
        qs = qs.filter(realized_at__date__lte=end_date)

    qs = (
        qs.annotate(day=TruncDate("realized_at"))
        .values("day")
        .annotate(pnl=Sum("pnl"))
        .order_by("day")
    )

    return [{"date": row["day"], "pnl": row["pnl"]} for row in qs]
