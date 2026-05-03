from django.test import TestCase, override_settings
from django.urls import reverse
from unittest.mock import patch

from payments.models import Item, Order


@override_settings(
    STRIPE_SECRET_KEY_DEFAULT="sk_test_fake",
    STRIPE_PUBLISHABLE_KEY_DEFAULT="pk_test_fake",
    STRIPE_CURRENCY_KEYPAIRS={"usd": {"secret": "", "publishable": ""}, "eur": {"secret": "", "publishable": ""}},
)
class PaymentViewsTests(TestCase):
    def setUp(self) -> None:
        self.item = Item.objects.create(
            name="Test Item",
            description="Test Description",
            price=5000,
            currency=Item.Currency.USD,
        )

    @patch("payments.views.create_payment_intent")
    def test_buy_item_returns_client_secret(self, mocked_create_intent):
        mocked_create_intent.return_value.id = "pi_test_123"
        mocked_create_intent.return_value.client_secret = "pi_test_123_secret_abc"

        response = self.client.get(reverse("payments:buy-item", args=[self.item.id]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"id": "pi_test_123", "client_secret": "pi_test_123_secret_abc"},
        )

    def test_item_page_contains_buy_button(self):
        response = self.client.get(reverse("payments:item-page", args=[self.item.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "buy-button")

    @patch("payments.views.create_payment_intent")
    def test_buy_order_returns_client_secret(self, mocked_create_intent):
        order = Order.objects.create()
        order.items.add(self.item)
        mocked_create_intent.return_value.id = "pi_test_order_123"
        mocked_create_intent.return_value.client_secret = "pi_test_order_123_secret_abc"

        response = self.client.get(reverse("payments:buy-order", args=[order.id]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"id": "pi_test_order_123", "client_secret": "pi_test_order_123_secret_abc"},
        )
