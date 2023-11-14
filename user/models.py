from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from .validators import CustomPasswordValidator
from django.utils.safestring import mark_safe

# Менеджер пользователей (Управляет созданием пользователей)
class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Укажите корректную почту')
        if not password:
            raise ValueError('Укажите пароль')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')
        return self.create_user(email, password, **extra_fields)
    
# Модель авторизации пользователей (Хранит информацию по данным для авторизации пользователей)
class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    password = models.CharField(
        ('password'),
        max_length=128,
        validators=[CustomPasswordValidator],
        help_text=mark_safe(CustomPasswordValidator().get_help_text()),
    )
    last_login_time = models.DateTimeField(null=True, blank=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    login_history = models.JSONField(default=list)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

# Модель типа пользователя (Хранит информацию по типам пользователям)
class UserType(models.Model):
    usertypedescription = models.CharField(max_length=50)

    def __str__(self):
       return self.usertypedescription

# Модель профиля пользователя (Хранит информацию по пользователям)
class UserProfile(models.Model):
    username = models.CharField(max_length=70)
    usersurname = models.CharField(max_length=70)
    userage = models.IntegerField(null=True, blank=True)
    userstatuspay = models.IntegerField(null=True)
    usertype = models.ForeignKey(UserType, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.username   
