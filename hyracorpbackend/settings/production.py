from django.utils.log import DEFAULT_LOGGING
import environ
import os
from pathlib import Path
from pythonjsonlogger import jsonlogger


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


# class LokiFormatter(jsonlogger.JsonFormatter):
#     def add_fields(self, log_record, record, message_dict):
#         super().add_fields(log_record, record, message_dict)
#         log_record["source"] = "django-app"  # Optional: Specify a source label
#         log_record["version"] = "1.0"  # Optional: Specify a version label


# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "formatters": {
#         "loki": {
#             "()": LokiFormatter,
#         },
#         "django.server": DEFAULT_LOGGING["formatters"]["django.server"],
#     },
#     "handlers": {
#         "console": {
#             "class": "logging.StreamHandler",
#             "formatter": "loki",
#         },
#         "loki": {
#             "class": "logging.handlers.HTTPHandler",
#             "formatter": "loki",
#             "url": LOKI_URL,
#             "method": "POST",
#         },
#         "django.server": DEFAULT_LOGGING["handlers"]["django.server"],
#     },
#     "loggers": {
#         "": {
#             "level": LOGLEVEL,
#             "handlers": ["console", "loki"],
#         },
#         "django.server": DEFAULT_LOGGING["loggers"]["django.server"],
#     },
# }
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "loki": {
            "level": "DEBUG",
            "class": "django.utils.log.HttpHandler",
            "url": LOKI_URL,
            "method": "POST",
            "labels": {"source": "hyracorp_backend"},  # Specify the source label
        },
    },
    "loggers": {
        "django": {
            "handlers": ["loki"],
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
