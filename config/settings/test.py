from __future__ import annotations

from .base import *

# GENERAL
# ------------------------------------------------------------------------------
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="django-insecure-&yvahr0=07+rhhegd-)_171)p29%9&m_w*i+&py0utt+*%ou&p",
)


# TEMPLATES
# ------------------------------------------------------------------------------
TEMPLATES[-1]["OPTIONS"]["loaders"] = [
    (
        "django.template.loaders.cached.Loader",
        [
            "django.template.loaders.filesystem.Loader",
            "django.template.loaders.app_directories.Loader",
        ],
    )
]


# TESTS
# ------------------------------------------------------------------------------
TEST_RUNNER = "django.test.runner.DiscoverRunner"


# EMAIL
# ------------------------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"


# PASSWORDS
# ------------------------------------------------------------------------------
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
