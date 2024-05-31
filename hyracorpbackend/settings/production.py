from django.utils.log import DEFAULT_LOGGING
import environ
import os
from pathlib import Path
from pythonjsonlogger import jsonlogger

BASE_DIR = Path(__file__).resolve().parent.parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

LOKI_URL = env("LOKI_URL")
LOGLEVEL = "INFO"
LOGGING_CONFIG = None


class LokiFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        log_record["source"] = "django-app"  # Optional: Specify a source label
        log_record["version"] = "1.0"  # Optional: Specify a version label


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "loki": {
            "()": LokiFormatter,
        },
        "django.server": DEFAULT_LOGGING["formatters"]["django.server"],
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "loki",
        },
        "loki": {
            "class": "logging.handlers.HTTPHandler",
            "formatter": "loki",
            "url": LOKI_URL,
            "method": "POST",
        },
        "django.server": DEFAULT_LOGGING["handlers"]["django.server"],
    },
    "loggers": {
        "": {
            "level": LOGLEVEL,
            "handlers": ["console", "loki"],
        },
        "django.server": DEFAULT_LOGGING["loggers"]["django.server"],
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
