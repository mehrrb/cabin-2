from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class CustomUserManager(UserManager):
    def create_superuser(self, phone, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('username', f'admin_{phone}')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone, email, password, **extra_fields)

    def create_user(self, phone, email, password=None, **extra_fields):
        if not phone:
            raise ValueError('The Phone field must be set')
        if not email:
            raise ValueError('The Email field must be set')
            
        email = self.normalize_email(email)
        username = extra_fields.pop('username', f'user_{phone}')
        user = self.model(phone=phone, email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class Account(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    phone = models.CharField(max_length=15, unique=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey()
    
    username = models.CharField(max_length=150, unique=True, blank=True)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    class Meta:
        db_table = 'cabin_account'

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = f"user_{self.phone}"
        super().save(*args, **kwargs)
