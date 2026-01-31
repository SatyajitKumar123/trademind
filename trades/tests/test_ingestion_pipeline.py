from decimal import Decimal
from io import StringIO

import pytest

from trades.models import RealizedTrade, Trade
from trades.services.ingestion_service import ingest_tradebook


@pytest.mark.django_db
def test_full_ingestion_pipeline():
    csv_data = """symbol,trade_type,quantity,price,order_execution_time
AAPL,BUY,10,100,2026-01-30T10:00:00
AAPL,SELL,10,120,2026-01-30T11:00:00
"""

    file = StringIO(csv_data)

    count = ingest_tradebook(file=file, broker="zerodha")

    assert Trade.objects.count() == 2
    assert RealizedTrade.objects.count() == 1
    assert count == 1

    realized = RealizedTrade.objects.first()
    assert realized.pnl == Decimal("200")
