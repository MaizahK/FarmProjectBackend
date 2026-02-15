from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('apps.auth.urls')),  # all /auth/* routes here
    path('animals/', include('apps.animals.urls')),  # all /animals/* routes here
]
