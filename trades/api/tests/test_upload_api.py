from io import BytesIO

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()


class TradeUploadAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )

        token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        self.url = reverse("trade-upload")

    def test_upload_trade_file_success(self):
        csv_content = (
            "symbol,trade_type,quantity,price,order_execution_time\n"
            "INFY,BUY,10,1500,2024-01-01T10:00:00\n"
            "INFY,SELL,10,1520,2024-01-01T11:00:00\n"
        )

        file = BytesIO(csv_content.encode("utf-8"))
        file.name = "test.csv"

        response = self.client.post(
            self.url,
            {"file": file, "broker": "zerodha"},
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("realized_trades", response.data)

    def test_duplicate_upload_blocked(self):
        csv_content = (
            "symbol,trade_type,quantity,price,order_execution_time\n"
            "INFY,BUY,10,1500,2024-01-01T10:00:00\n"
            "INFY,SELL,10,1520,2024-01-01T11:00:00\n"
        )

        file1 = BytesIO(csv_content.encode("utf-8"))
        file1.name = "test.csv"

        file2 = BytesIO(csv_content.encode("utf-8"))
        file2.name = "test.csv"

        self.client.post(
            self.url, {"file": file1, "broker": "zerodha"}, format="multipart"
        )
        response = self.client.post(
            self.url, {"file": file2, "broker": "zerodha"}, format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
