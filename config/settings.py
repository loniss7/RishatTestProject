import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    "django-insecure-dev-key-change-me",
)
DEBUG = os.getenv("DJANGO_DEBUG", "true").lower() == "true"
ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")
    if host.strip()
]
railway_public_domain = os.getenv("RAILWAY_PUBLIC_DOMAIN", "").strip()
if railway_public_domain and railway_public_domain not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(railway_public_domain)
if ".up.railway.app" not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(".up.railway.app")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "payments",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "DJANGO_CSRF_TRUSTED_ORIGINS",
        "http://127.0.0.1,http://localhost,https://127.0.0.1,https://localhost",
    ).split(",")
    if origin.strip()
]

if railway_public_domain:
    railway_origin = f"https://{railway_public_domain}"
    if railway_origin not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(railway_origin)
if "https://*.up.railway.app" not in CSRF_TRUSTED_ORIGINS:
    CSRF_TRUSTED_ORIGINS.append("https://*.up.railway.app")

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

STRIPE_SECRET_KEY_DEFAULT = os.getenv(
    "STRIPE_SECRET_KEY_DEFAULT",
    os.getenv("STRIPE_SECRET_KEY", ""),
)
STRIPE_PUBLISHABLE_KEY_DEFAULT = os.getenv(
    "STRIPE_PUBLISHABLE_KEY_DEFAULT",
    os.getenv("STRIPE_PUBLISHABLE_KEY", ""),
)

STRIPE_CURRENCY_KEYPAIRS = {
    "usd": {
        "secret": os.getenv("STRIPE_SECRET_KEY_USD", ""),
        "publishable": os.getenv("STRIPE_PUBLISHABLE_KEY_USD", ""),
    },
    "eur": {
        "secret": os.getenv("STRIPE_SECRET_KEY_EUR", ""),
        "publishable": os.getenv("STRIPE_PUBLISHABLE_KEY_EUR", ""),
    },
}
