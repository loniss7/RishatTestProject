from django.contrib import admin

from payments.models import Discount, Item, Order, Tax


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "currency")
    search_fields = ("name",)


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "stripe_coupon_id")
    search_fields = ("name", "stripe_coupon_id")


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "stripe_tax_rate_id")
    search_fields = ("name", "stripe_tax_rate_id")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "discount", "tax")
    filter_horizontal = ("items",)
