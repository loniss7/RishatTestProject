from django.core.exceptions import ImproperlyConfigured
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.http import require_GET

import stripe

from payments.models import Item, Order
from payments.stripe_utils import (
    create_payment_intent,
    get_stripe_publishable_key_for_currency,
    get_stripe_secret_key_for_currency,
)


def _payment_error_response(error: Exception) -> JsonResponse:
    return JsonResponse({"error": str(error)}, status=500)


@require_GET
def item_page(request: HttpRequest, item_id: int) -> HttpResponse:
    item = get_object_or_404(Item, pk=item_id)
    publishable_key = ""
    stripe_error = ""
    try:
        publishable_key = get_stripe_publishable_key_for_currency(item.currency)
    except ImproperlyConfigured as exc:
        stripe_error = str(exc)

    return render(
        request,
        "payments/item.html",
        {
            "item": item,
            "publishable_key": publishable_key,
            "stripe_available": bool(publishable_key),
            "stripe_error": stripe_error,
            "buy_url": reverse("payments:buy-item", args=[item.id]),
        },
    )


@require_GET
def order_page(request: HttpRequest, order_id: int) -> HttpResponse:
    order = get_object_or_404(Order.objects.prefetch_related("items"), pk=order_id)
    items = list(order.items.all())
    if not items:
        return HttpResponse("Order has no items.", status=400)

    base_currency = items[0].currency
    if any(item.currency != base_currency for item in items):
        return HttpResponse("Order contains multiple currencies.", status=400)

    publishable_key = ""
    stripe_error = ""
    try:
        publishable_key = get_stripe_publishable_key_for_currency(base_currency)
    except ImproperlyConfigured as exc:
        stripe_error = str(exc)

    return render(
        request,
        "payments/order.html",
        {
            "order": order,
            "items": items,
            "publishable_key": publishable_key,
            "stripe_available": bool(publishable_key),
            "stripe_error": stripe_error,
            "buy_url": reverse("payments:buy-order", args=[order.id]),
            "total": sum(item.price for item in items),
            "currency": base_currency.upper(),
        },
    )


@require_GET
def buy_item(request: HttpRequest, item_id: int) -> JsonResponse:
    item = get_object_or_404(Item, pk=item_id)

    try:
        secret_key = get_stripe_secret_key_for_currency(item.currency)
        payment_intent = create_payment_intent(
            secret_key=secret_key,
            amount=item.price,
            currency=item.currency,
            metadata={"item_id": str(item.id)},
        )
    except (stripe.error.StripeError, ImproperlyConfigured) as exc:
        return _payment_error_response(exc)

    return JsonResponse(
        {
            "id": payment_intent.id,
            "client_secret": payment_intent.client_secret,
        }
    )


@require_GET
def buy_order(request: HttpRequest, order_id: int) -> JsonResponse:
    order = get_object_or_404(Order.objects.select_related("discount", "tax"), pk=order_id)
    items = list(order.items.all())
    if not items:
        return JsonResponse({"error": "Order has no items."}, status=400)

    currency = items[0].currency
    if any(item.currency != currency for item in items):
        return JsonResponse({"error": "Order contains multiple currencies."}, status=400)

    amount = sum(item.price for item in items)
    metadata = {"order_id": str(order.id)}
    if order.discount:
        metadata["discount_coupon_id"] = order.discount.stripe_coupon_id
    if order.tax:
        metadata["tax_rate_id"] = order.tax.stripe_tax_rate_id

    try:
        secret_key = get_stripe_secret_key_for_currency(currency)
        payment_intent = create_payment_intent(
            secret_key=secret_key,
            amount=amount,
            currency=currency,
            metadata=metadata,
        )
    except (stripe.error.StripeError, ImproperlyConfigured) as exc:
        return _payment_error_response(exc)

    return JsonResponse(
        {
            "id": payment_intent.id,
            "client_secret": payment_intent.client_secret,
        }
    )
