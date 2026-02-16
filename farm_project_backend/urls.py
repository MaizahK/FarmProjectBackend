from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.identity.urls')),
    path('api/users/', include('apps.users.urls')),
    path('api/animals/', include('apps.animals.urls')),
    # path('api/resources/', include('apps.resources.urls')),
    # path('api/products/', include('apps.products.urls')),
]
