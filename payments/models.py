from django.db import models


class Item(models.Model):
    class Currency(models.TextChoices):
        USD = "usd", "USD"
        EUR = "eur", "EUR"

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.PositiveIntegerField(help_text="Price in the smallest currency unit")
    currency = models.CharField(
        max_length=3,
        choices=Currency.choices,
        default=Currency.USD,
    )

    def __str__(self) -> str:
        return f"{self.name} ({self.price} {self.currency.upper()})"


class Discount(models.Model):
    name = models.CharField(max_length=255)
    stripe_coupon_id = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class Tax(models.Model):
    name = models.CharField(max_length=255)
    stripe_tax_rate_id = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class Order(models.Model):
    items = models.ManyToManyField(Item, related_name="orders")
    discount = models.ForeignKey(
        Discount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )
    tax = models.ForeignKey(
        Tax,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Order #{self.pk}"
