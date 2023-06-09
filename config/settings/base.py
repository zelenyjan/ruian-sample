from __future__ import annotations

from pathlib import Path

from django.utils.translation import gettext_lazy as _

import environ

PROJECT_NAME = "ruian"

BASE_DIR = Path(__file__).resolve().parent.parent.parent
APPS_DIR = BASE_DIR / PROJECT_NAME


env = environ.Env()
READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=True)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(BASE_DIR / ".env"))


# GENERAL
# ------------------------------------------------------------------------------
DEBUG = env.bool("DJANGO_DEBUG", False)
BASE_URL = env("BASE_URL", default="http://127.0.0.1:8000")


# APPS
# ------------------------------------------------------------------------------
INSTALLED_APPS = [
    "ruian.users",
    "ruian.data",
    "rest_framework",
    "webpack_loader",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
]


# MIDDLEWARE
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# TEMPLATES
# ------------------------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n",
                "django.template.context_processors.static",
            ],
        },
    },
]


# EMAILS
# ------------------------------------------------------------------------------
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="ruian@zeleny.dev")
SERVER_EMAIL = env("SERVER_EMAIL", default=DEFAULT_FROM_EMAIL)


# ADMIN
# ------------------------------------------------------------------------------
DJANGO_ADMIN_URL = "admin/"
ADMINS = [("Jan Zelený", "jan@zeleny.io")]
MANAGERS = ADMINS


# INTERNATIONALIZATION
# ------------------------------------------------------------------------------
TIME_ZONE = "Europe/Prague"
LANGUAGE_CODE = "cs"
USE_I18N = True
USE_TZ = True
LANGUAGES = [
    ("cs", _("Čeština")),
]


# DATABASES
# ------------------------------------------------------------------------------
DATABASES = {"default": env.db("DATABASE_URL", default=f"postgres:///{PROJECT_NAME}")}
DATABASES["default"]["ATOMIC_REQUESTS"] = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# FIXTURES
# ------------------------------------------------------------------------------
FIXTURE_DIRS = [BASE_DIR / "fixtures"]


# LOCALE
# ------------------------------------------------------------------------------
LOCALE_PATHS = [BASE_DIR / "locale"]


# CACHES
# ------------------------------------------------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}


# URLS
# ------------------------------------------------------------------------------
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"


# AUTHENTICATION
# ------------------------------------------------------------------------------
AUTH_USER_MODEL = "users.User"


# PASSWORDS
# ------------------------------------------------------------------------------
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.ScryptPasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# SECURITY
# ------------------------------------------------------------------------------
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = False
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"


# STATIC
# ------------------------------------------------------------------------------
USE_DEV_STATIC = env.bool("USE_DEV_STATIC", default=True)

DEV_STATICFILES_DIR = BASE_DIR / "static" / "dist" / "dev"
PROD_STATICFILES_DIR = BASE_DIR / "static" / "dist" / "prod"

if USE_DEV_STATIC:
    STATICFILES_DIRS = [DEV_STATICFILES_DIR]
else:
    STATICFILES_DIRS = [PROD_STATICFILES_DIR]

STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = "/static/"
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"


# MEDIA
# ------------------------------------------------------------------------------
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"
FILE_UPLOAD_PERMISSIONS = 0o664
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o775
DEFAULT_FILE_STORAGE = "config.storages.MediaStorage"


# DRF
# ------------------------------------------------------------------------------
REST_FRAMEWORK = {
    "DATETIME_FORMAT": "%d. %m. %Y %H:%M:%S",
    "DATE_FORMAT": "%d. %m. %Y",
    "TIME_FORMAT": "%H:%M:%S",
}


# WEBPACK_LOADER
# ------------------------------------------------------------------------------
# should match with `const apps` in webpack.config.js
WEBPACK_APPS = [PROJECT_NAME]


def get_dev_webpack_loader_config() -> dict[str, dict]:
    apps = {}
    for app in WEBPACK_APPS:
        if USE_DEV_STATIC:
            stats_file = BASE_DIR / "templates" / "webpack" / f"stats.{app}.dev.json"
        else:
            stats_file = BASE_DIR / "templates" / "webpack" / f"stats.{app}.prod.json"
        apps["DEFAULT" if app == PROJECT_NAME else app.upper()] = {
            "CACHE": False,
            "BUNDLE_DIR_NAME": f"{app}/",
            "STATS_FILE": stats_file,
            "POLL_INTERVAL": 0.1,
            "IGNORE": [r".+\.hot-update.js", r".+\.map"],
        }
    return apps


WEBPACK_LOADER = get_dev_webpack_loader_config()
