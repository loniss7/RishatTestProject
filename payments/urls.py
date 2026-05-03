from django.urls import path

from payments import views

app_name = "payments"

urlpatterns = [
    path("item/<int:item_id>/", views.item_page, name="item-page"),
    path("buy/<int:item_id>/", views.buy_item, name="buy-item"),
    path("order/<int:order_id>/", views.order_page, name="order-page"),
    path("buy/order/<int:order_id>/", views.buy_order, name="buy-order"),
]
