"""Project urls."""

# Third Party
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.urls import path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

# Project
from orp_apps.orp_api.utils import LoginView

schema_view = get_schema_view(
    openapi.Info(
        title='ORP API',
        description='ORP API',
        default_version='1.0'
    ),
    public=True,
)


urlpatterns = [
    path('api/<str:version>/', include('orp_apps.orp_api.urls')),
    path('auth/login/', LoginView.as_view(), name='login'),
    re_path(
        r'^doc(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('doc/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
