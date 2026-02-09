from django.urls import path
from .views import LoginAPIView, LogoutAPIView, SignUpAPIView

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('signup/', SignUpAPIView.as_view(), name='signup'),
]
