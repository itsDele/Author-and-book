from django.contrib import admin
from django.urls import path, include,re_path

from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger schema view
schema_view = get_schema_view(
    openapi.Info(
        title="My APIs",  # Customize: Your API name
        default_version='v1',  # Version
        description="A sample API for Swagger docs",  # Description
    ),
    public=True,  # Allow unauth access to docs
    permission_classes=(permissions.AllowAny,),  # Or restrict
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("books/", include("book.urls")),
    path("author/", include("authors.urls")),
    # Swagger UI
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # ReDoc alternative (fancier docs)
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
