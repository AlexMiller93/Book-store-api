from django.urls import path
from accounts.views import (
    RegistrationAPIView, 
    LoginAPIView, 
    UserRetrieveUpdateAPIView
    )
# from rest_framework_simplejwt import views as jwt_views

app_name = 'accounts'

urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view()),
    path('users/', RegistrationAPIView.as_view()),
    path('users/login/', LoginAPIView.as_view()),
    
    # re_path(r'^registration/?$', RegistrationAPIView.as_view(), name='user_registration'),
    # re_path(r'^login/?$', LoginAPIView.as_view(), name='user_login'),
]
