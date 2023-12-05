from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ROLE = (("A", "Admin"), ("U", "User"))

    email = models.EmailField(max_length=150, unique=True)
    phone = models.CharField(max_length=10, unique=True)
    role = models.CharField(max_length=1, choices=ROLE)
    
    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone"]

    def __str__(self):
        return self.email
    
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
