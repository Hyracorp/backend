import environ
import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "whitenoise.runserver_nostatic",
    "admin_panel",
    "property_management",
    "user_auth",
    "user_profile",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    # Add whitenoise middleware here
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# LOGGER CONFIG


LOKI_URL = env("LOKI_URL")
LOGGING_CONFIG = None


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}

ALLOWED_HOSTS = [env("SERVER_DOMAIN"), env("SERVER_IP"), "0.0.0.0"]
# temp testing config
CORS_ALLOW_ALL_ORIGINS = True
CSRF_COOKIE_SECURE = False
CSRF_TRUSTED_ORIGINS = []

# production config to apply

# CORS_ALLOWED_ORIGINS = [
#     env("APP_URL"),
#     env("SERVER_URL"),
# ]
# CSRF_COOKIE_SECURE = True
# CSRF_TRUSTED_ORIGINS = [
#     env("APP_URL"),
# ]
