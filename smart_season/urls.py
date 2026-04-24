from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from fields.views import dashboard as fields_dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", fields_dashboard, name="home"),
    path("users/", include("users.urls", namespace="users")),
    path("fields/", include("fields.urls", namespace="fields")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)