from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.identity.urls')),
    path('', include('apps.users.urls')),
    path('', include('apps.animals.urls')),
    path('', include('apps.resources.urls')),
    path('', include('apps.products.urls')),
]
