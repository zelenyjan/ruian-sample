from __future__ import annotations

from django.conf import settings
from django.contrib import admin
from django.urls import include, path


def trigger_error(request):  # noqa
    return 1 / 0


urlpatterns = [
    path("sentry-debug/", trigger_error),
    path("", include("ruian.data.urls")),
    path("api/data/", include("ruian.data.api.urls")),
    path(settings.DJANGO_ADMIN_URL, admin.site.urls),
]
