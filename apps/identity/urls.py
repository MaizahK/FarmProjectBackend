from django.urls import path
from .views import LogoutView, TokenObtainPairView, TokenVerifyView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutView.as_view(), name='token_logout'),
    path('verify/', TokenVerifyView.as_view(), name='token_verify'),
]