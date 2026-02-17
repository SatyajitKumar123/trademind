from decimal import Decimal
from io import StringIO

import pytest
from django.contrib.auth import get_user_model

from trades.models import RealizedTrade, Trade
from trades.services.ingestion_service import ingest_tradebook

User = get_user_model()


@pytest.mark.django_db
def test_full_ingestion_pipeline():
    user = User.objects.create_user(username="testuser", password="pass")

    csv_data = """symbol,trade_type,quantity,price,order_execution_time
AAPL,BUY,10,100,2026-01-30T10:00:00
AAPL,SELL,10,120,2026-01-30T11:00:00
"""

    file = StringIO(csv_data)

    count = ingest_tradebook(user=user, file=file, broker="zerodha")

    assert Trade.objects.filter(user=user).count() == 2
    assert RealizedTrade.objects.filter(user=user).count() == 1
    assert count == 1

    realized = RealizedTrade.objects.first()
    assert realized.pnl == Decimal("200")
