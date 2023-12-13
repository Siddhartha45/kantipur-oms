from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    ROLE = (("A", "Admin"), ("U", "User"))

    email = models.EmailField(max_length=150, unique=True)
    phone = models.CharField(max_length=10, unique=True)
    role = models.CharField(max_length=1, choices=ROLE)
    token = models.CharField(max_length=200)
    is_verified = models.BooleanField(default=False)
    
    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone"]
    
    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class GeneratedPinNumber(models.Model):
    pin = models.IntegerField(unique=True)
    
    def __str__(self):
        return self.pin