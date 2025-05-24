from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from utils.validations import validate_phone, validate_username
from django.db import models

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(
        max_length=11, unique=True, validators=[validate_phone]
    )
    email = models.EmailField(
        unique=True, blank=True, null=True
    )
    username = models.CharField(
        max_length=80, unique=True, blank=True, null=True, validators=[validate_username]
    )

    created_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified  = models.BooleanField(default=False)
    

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email', 'username']

    objects = UserManager()

    @property
    def is_staff(self):
        return self.is_admin

    def __str__(self):
        return f'{self.phone}'


class Profile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile = models.ImageField(upload_to='user/profile', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    first_name = models.CharField(max_length=60, blank=True, null=True)
    last_name = models.CharField(max_length=60, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)


    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def __str__(self):
        return f'{self.user}'
    

class OTP(models.Model):
    phone = models.CharField(max_length=11)
    code = models.CharField(max_length=6)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.phone