from django.test import TestCase
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APIClient

# Create your tests here.

# python3 manage.py test books.tests.test_views


# тест авторизации 

#! регистрация

#? http://127.0.0.1:8000/api/v1/auth/users/
# * username, password

#! вход в систему

#? http://127.0.0.1:8000/auth/token/login/
# * username, password

class AuthenticationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(
            username=self.username, password=self.password)
        
    def test_registration(self):
        # Проверка регистрации пользователя
        url = '/users/'
        data = {
            'username': self.username,
            'password': self.password,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('id' in response.data)
        self.assertTrue('username' in response.data)
        self.assertTrue('password' in response.data)
    
    # def test_login(self):
    #     # Проверка входа пользователя
    #     url = '/auth/jwt/create/'
    #     data = {'username': self.username, 'password': self.password}
    #     response = self.client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertTrue('access' in response.data)
    #     self.assertTrue('refresh' in response.data)