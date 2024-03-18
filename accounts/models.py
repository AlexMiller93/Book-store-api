import jwt

from datetime import datetime, timedelta
from django.conf import settings
from django.db import models
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from accounts.managers import UserManager

# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    """ """
    username = models.CharField(db_index=True, max_length=255, unique=True)
    
    email = models.EmailField(
        validators=[validators.validate_email],
        unique=True,
        blank=False
    )
    
    is_staff = models.BooleanField(default=False)
    
    is_active = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = ('username',)
    
    
    objects = UserManager()
    
    def __str__(self):
        return self.username
    
    @property
    def token(self):
        return self._generate_jwt_token()
    
    def get_full_name(self):
        return self.username
    
    def get_short_name(self):
        return self.username
    
    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=60)
        
        token = jwt.encode({
            'id': self.pk,
            'exp': dt.utcfromtimestamp(dt.timestamp())
        }, settings.SECRET_KEY, algorithm='HS256')
        
        return token.decode('utf-8')