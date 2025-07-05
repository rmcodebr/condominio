from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
  openapi.Info(
    title="Condominio API",
    default_version='v1',
    description='Gerenciamento de Condominio API',
    contact=openapi.Contact(email="contact@rmcode.org"),
    license=openapi.License(name='MIT License')    
  ),
  public=True,
  permission_classes=[permissions.AllowAny,],
)

urlpatterns = [
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    path('admin/', admin.site.urls),

    path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/auth/', include('accounts.urls')),

]

admin.site.site_header="Condominio"
admin.site.site_title="Condominio Portal"
admin.site.index_title="Welcome to Condominio Portal"

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
