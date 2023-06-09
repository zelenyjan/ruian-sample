from __future__ import annotations

from django.urls import path

from ruian.data.views import IndexTemplateView

app_name = "data"
urlpatterns = [
    path("", IndexTemplateView.as_view(), name="data_index"),
]
