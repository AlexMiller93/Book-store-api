from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from accounts.serializers import LoginSerializer, RegistrationSerializer

class RegistrationAPIView(APIView):
    """ Регистрация новых пользователей """
    
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer
    
    def post(self, request):
        """ 
            Создает объект пользователя
            Имя пользователя, адрес электронной почты и пароль обязательны для ввода.
            Возвращает JSON веб токен.
        """
        
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(
            {
                'token': serializer.data.get('token', None)
            }, status = status.HTTP_201_CREATED,
        )
        
class LoginAPIView(APIView):
    """ Проверяет данные пользователя перед входом в систему """
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    
    def post(self, request):
        """ 
            Проверяет существует ли пользователь с введенными данными.
            Возвращает JSON веб токен.
        """
        
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)