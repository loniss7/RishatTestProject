import stripe
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def get_stripe_secret_key_for_currency(currency: str) -> str:
    currency = currency.lower()
    keypair = settings.STRIPE_CURRENCY_KEYPAIRS.get(currency, {})
    secret_key = keypair.get("secret") or settings.STRIPE_SECRET_KEY_DEFAULT
    if not secret_key:
        raise ImproperlyConfigured(
            f"Stripe secret key is not configured for currency '{currency}'."
        )
    return secret_key


def get_stripe_publishable_key_for_currency(currency: str) -> str:
    currency = currency.lower()
    keypair = settings.STRIPE_CURRENCY_KEYPAIRS.get(currency, {})
    publishable_key = keypair.get("publishable") or settings.STRIPE_PUBLISHABLE_KEY_DEFAULT
    if not publishable_key:
        raise ImproperlyConfigured(
            f"Stripe publishable key is not configured for currency '{currency}'."
        )
    return publishable_key


def create_payment_intent(
    *,
    secret_key: str,
    amount: int,
    currency: str,
    metadata: dict[str, str] | None = None,
) -> stripe.PaymentIntent:
    stripe.api_key = secret_key
    payload: dict = {
        "amount": amount,
        "currency": currency.lower(),
        "payment_method_types": ["card"],
    }
    if metadata:
        payload["metadata"] = metadata
    return stripe.PaymentIntent.create(**payload)
