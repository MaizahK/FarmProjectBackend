from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('apps.identity.urls')),
    path('api/users/', include('users.urls')),
    path('api/animals/', include('animals.urls')),
    path('api/resources/', include('resources.urls')),]
