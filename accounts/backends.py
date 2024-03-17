import jwt

from django.conf import settings
from rest_framework import authentication, exceptions

from accounts.models import User

class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Bearer'
    
    def authenticate(self, request):
        """ 
        Метод аутентификации для каждого запроса, 
        где требуется аутентификация пользователя
        
        Возвращает 2 варианта значений:
            - None - когда аутентификация не пройдена, 
            к примеру когда в запросе не было токена
            
            - (user, token) - кортеж из имени пользователя и токена, 
                аутентификация успешно пройдена        
        
        """
        request.user = None
        
        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()
        
        if not auth_header:
            return None
        
        if len(auth_header) == 1:
            # некорректный токен заголовок. Данные не предоставлены.
            return None
        
        elif len(auth_header) > 2:
            # некорректный токен заголовок
            return None
        
        # нужно декодировать prefix и token
        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')
        
        if prefix.lower() != auth_header_prefix:
            return None
        
        return self._authenticate_credentials(request, token)
    
    def _authenticate_credentials(self, request, token):
        """ Метод для аутентификации по данному токену.
            Если успешно, возвращает имя пользователя и токен.
            Если нет, вызывает ошибку.
        """
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except:
            msg = 'Некорректная аутентификация. Нельзя декодировать токен'
            raise exceptions.AuthenticationFailed(msg)
        
        try:
            user = User.objects.get(pk=payload['id'])
        except User.DoesNotExist:
            msg = 'Нет пользователя по заданному токену'
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = 'Пользователь деактивирован'
            raise exceptions.AuthenticationFailed(msg)

        return (user, token)
    