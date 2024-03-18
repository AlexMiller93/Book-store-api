from django.urls import path
from dj_rest_auth.jwt_auth import get_refresh_view
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView

from rest_framework_simplejwt.views import TokenVerifyView

from accounts.views import (
    RegistrationAPIView, 
    LoginAPIView, 
    UserRetrieveUpdateAPIView
    )
# from rest_framework_simplejwt import views as jwt_views

app_name = 'accounts'

urlpatterns = [
    # path('user/', UserRetrieveUpdateAPIView.as_view()),
    # path('users/', RegistrationAPIView.as_view()),
    # path('users/login/', LoginAPIView.as_view()),
    
    path("register/", RegisterView.as_view(), name="rest_register"),
    path("login/", LoginView.as_view(), name="rest_login"),
    path("logout/", LogoutView.as_view(), name="rest_logout"),
    path("user/", UserDetailsView.as_view(), name="rest_user_details"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("token/refresh/", get_refresh_view().as_view(), name="token_refresh"),
    
    # re_path(r'^registration/?$', RegistrationAPIView.as_view(), name='user_registration'),
    # re_path(r'^login/?$', LoginAPIView.as_view(), name='user_login'),
]
