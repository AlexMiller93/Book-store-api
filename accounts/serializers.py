from rest_framework import serializers

from django.contrib.auth import authenticate

from accounts.models import User
from accounts.backends import JWTAuthentication


class RegistrationSerializer(serializers.ModelSerializer):
    """ 
        Создает нового пользователя.
        
        Имя пользователя, адрес электронной почты и пароль обязательны для ввода.
        Возвращает JSON веб токен
    """
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
    )
    
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'token',)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class LoginSerializer(serializers.Serializer):
    """ 
        Проверяет данные существующего пользователя.
        
        Адрес электронной почты и пароль обязательны для входа в аккаунт.
        Возвращает JSON веб токен.
    """
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)

    # Игнорировать поля если они не включены в запрос
    username = serializers.CharField(max_length=255, read_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    
    def validate(self, data):
        """
        Проверяет данные пользователя
        """
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'Необходим адрес электронной почты для входа в аккаунт.'
            )

        if password is None:
            raise serializers.ValidationError(
                'Необходим пароль для входа в аккаунт.'
            )

        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'Пользователь с таким адресом электронной почты и паролем не найден.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'Пользователь не активирован.'
            )

        return {
            'token': user.token,
        }