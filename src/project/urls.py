from django.urls import path, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    path("tasks/", include("tasks.urls"), name="tasks"),
    path("tokens/", include("tokens.urls"), name="tokens"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_URL)

if settings.URL_PREFIX:
    # If there is a URL prefix, add to all.
    # Used for being behind a proxy / url prefix.
    urlpatterns = [path(f"{settings.URL_PREFIX}/", include(urlpatterns))]
