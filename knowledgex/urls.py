# knowledgex/urls.py
from django.contrib import admin
from django.urls import path, include
from core.views import home

urlpatterns = [
    path("admin/", admin.site.urls),

    # Home
    path("", home, name="home"),

    # Core app (if you have extra core URLs)
    path("", include("core.urls")),

    # Accounts
    path("accounts/", include("accounts.urls")),

    # ✅ Resources – simple include, NO namespace here
    path("resources/", include("resources.urls")),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
