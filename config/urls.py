from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("registry.api_urls")),
    path("", include("registry.urls")),
]
