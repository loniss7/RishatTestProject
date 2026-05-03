# Django + Stripe (PaymentIntent)

Минимальный сервис на Django для оплаты `Item` и `Order` через Stripe Payment Intents.

## Требования

- Python 3.13+

## Переменные окружения (`.env`)

```env
DJANGO_SECRET_KEY=change-me
DJANGO_DEBUG=true
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

STRIPE_SECRET_KEY_DEFAULT=sk_test_...
STRIPE_PUBLISHABLE_KEY_DEFAULT=pk_test_...
```

Опционально (ключи по валютам):

```env
STRIPE_SECRET_KEY_USD=sk_test_...
STRIPE_PUBLISHABLE_KEY_USD=pk_test_...
STRIPE_SECRET_KEY_EUR=sk_test_...
STRIPE_PUBLISHABLE_KEY_EUR=pk_test_...
```

## Локальный запуск

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Админка: `http://localhost:8000/admin/`

## Docker

```bash
docker compose up --build
```

## Эндпоинты

- `GET /item/<item_id>/` — страница оплаты одного товара
- `GET /buy/<item_id>/` — создать PaymentIntent (`id`, `client_secret`)
- `GET /order/<order_id>/` — страница оплаты заказа
- `GET /buy/order/<order_id>/` — создать PaymentIntent для заказа
- `GET /admin/` — Django Admin

## Быстрая проверка

1. В админке создайте `Item` (например `price=1000`, `currency=USD`).
2. Откройте `/item/<id>/` и оплатите тестовой картой `4242 4242 4242 4242` (любая будущая дата/CVC).

