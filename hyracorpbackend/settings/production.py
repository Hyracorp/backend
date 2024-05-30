from django.utils.log import DEFAULT_LOGGING

ALLOWED_HOSTS = ["server.hyracorp.com", "192.3.61.155", "0.0.0.0"]

LOGGING_CONFIG = None
LOGLEVEL = "INFO"
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        # Use JSON formatter as default
        "default": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
        },
        "django.server": DEFAULT_LOGGING["formatters"]["django.server"],
    },
    "handlers": {
        # Route console logs to stdout
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        "django.server": DEFAULT_LOGGING["handlers"]["django.server"],
    },
    "loggers": {
        # Default logger for all Python modules
        "": {
            "level": LOGLEVEL,
            "handlers": [
                "console",
            ],
        },
        # Default runserver request logging
        "django.server": DEFAULT_LOGGING["loggers"]["django.server"],
    },
}
