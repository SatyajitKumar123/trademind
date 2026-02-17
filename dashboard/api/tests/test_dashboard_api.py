from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()


class DashboardAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(username="testuser", password="pass")

        token = AccessToken.for_user(self.user)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_dashboard_summary_endpoint(self):
        url = reverse("api-dashboard-summary")
        response = self.client.get(url)

        self.assertIn(response.status_code, [200, 404])
        self.assertEqual(response["Content-Type"], "application/json")

    def test_equity_curve_endpoint(self):
        url = reverse("api-equity-curve")
        response = self.client.get(url)

        self.assertIn(response.status_code, [200, 404])
        self.assertEqual(response["Content-Type"], "application/json")

    def test_risk_metrics_endpoint(self):
        url = reverse("api-risk-metrics")
        response = self.client.get(url)

        self.assertIn(response.status_code, [200, 404])
        self.assertEqual(response["Content-Type"], "application/json")
