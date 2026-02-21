from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView # Import this
from .views import LogoutView, TokenObtainPairView, TokenVerifyView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'), # Add this
    path('logout/', LogoutView.as_view(), name='token_logout'),
    path('verify/', TokenVerifyView.as_view(), name='token_verify'),
]