from __future__ import annotations

from .base import *  # noqa

# GENERAL
# ------------------------------------------------------------------------------
DEBUG = True
SECRET_KEY = "django-insecure-jafr+3z+xs!x4v3-b-y_vi4-&59_f%fbqme=)g4z06(py79h#y"
ALLOWED_HOSTS = ["*"]
CSRF_TRUSTED_ORIGINS = ["https://ruian.zeleny.dev"]


# EMAILS
# ------------------------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# LOGGING
# ------------------------------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "komplexnizdravi": {"()": "config.logging.RuianFormatter"},
        "colorama": {"()": "config.logging.ColoramaFormatter"},
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "colorama",
        },
    },
    "root": {"level": "DEBUG", "handlers": ["console"]},
    "loggers": {
        "django.db.backends": {"level": "INFO"},
        "PIL.Image": {"level": "INFO"},
    },
}
