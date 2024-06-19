from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title="Boxproduction",
        default_version='v1',
        description='Box Project',
        terms_of_service='demo.uz',
        contact=openapi.Contact(email='sanjarwer93@gmail.com'),
        license=openapi.License(name="demo license")
    ),
    public=True,
    permission_classes=[permissions.AllowAny],

)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.production.view_production.urls')),
    path('api/', include('apps.production.urls')),
    path('api/info/', include('apps.info.urls')),
    path('api/depo/', include('apps.depo.urls')),

    # dj-rest-auth
    path('api-auth/', include('rest_framework.urls')),
    path('api/rest-auth/', include('dj_rest_auth.urls')),
    path('api/rest-auth/registration', include('dj_rest_auth.registration.urls')),

    # swagger
    path('swagger/', schema_view.with_ui(
        'swagger', cache_timeout=0), name='swagger-swagger-ui')

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
