from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from trades.models import Trade

User = get_user_model()


class TradeModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="pass")

    def test_trade_value_calculation(self):
        trade = Trade.objects.create(
            user=self.user,
            symbol="AAPL",
            side=Trade.Side.BUY,
            quantity=10,
            price=Decimal("150.50"),
            executed_at=timezone.now(),
        )

        self.assertEqual(trade.trade_value, Decimal("1505.00"))

    def test_trade_string_representation(self):
        trade = Trade.objects.create(
            user=self.user,
            symbol="TSLA",
            side=Trade.Side.SELL,
            quantity=5,
            price=Decimal("700.00"),
            executed_at=timezone.now(),
        )

        self.assertIn("TSLA", str(trade))
