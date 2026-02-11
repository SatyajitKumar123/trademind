from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient


class DashboardAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

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
