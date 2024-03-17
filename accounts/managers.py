from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True
    
    def _create_user(self, username, email, password=None, **extra_fields):
        """ 
        Создает и сохраняет пользователя с введенным именем пользователя,
        адресом электронной почты и паролем
        """
        
        if not username:
            raise ValueError('Необходимо ввести имя пользователя')
        
        if not email:
            raise ValueError('Необходимо ввести почту')
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_user(self, username,  email, password=None, **extra_fields):
        """ 
        Создает и возвращает `User` с адресом электронной почты,
        именем пользователя и паролем. 
        """
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        return self._create_user(username, email, password, **extra_fields)
    
    def create_superuser(self, username, email, password, **extra_fields):
        """ 
        Создает и возвращает пользователя с правами суперпользователя (администратора).
        """
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')
        
        return self._create_user(username, email, password, **extra_fields)