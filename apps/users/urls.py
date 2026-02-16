from django.urls import path
from .views import RoleViewSet, UserViewSet

urlpatterns = [
    path('roles/', RoleViewSet.as_view({'get': 'list', 'post': 'create'}), name='roles'),
    path('roles/<int:pk>/', RoleViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='role-detail'),
    path('users/', UserViewSet.as_view({'get': 'list', 'post': 'create'}), name='users'),
    path('users/<int:pk>/', UserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='user-detail'),
]