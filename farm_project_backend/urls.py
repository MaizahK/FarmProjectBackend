from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.identity.urls')),
    path('', include('apps.users.urls')),
    path('', include('apps.animals.urls')),
    path('', include('apps.resources.urls')),
    path('', include('apps.products.urls')),
    path('', include('apps.logs.urls')),
    path('', include('apps.inventory.urls')),
    path('', include('apps.finances.urls')),
    path('', include('apps.employees.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
