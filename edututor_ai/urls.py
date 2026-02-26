from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("edututor_ai.web_urls")),
    path("api/accounts/", include("accounts.urls")),
    path("api/chat/", include("chat.urls")),
    path("api/documents/", include("documents.urls")),
    path("api/subscriptions/", include("subscriptions.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
