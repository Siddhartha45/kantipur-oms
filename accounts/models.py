from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ROLE = (("A", "Admin"), ("U", "User"))

    email = models.EmailField(max_length=150, unique=True)
    phone = models.CharField(max_length=10, unique=True)
    role = models.CharField(max_length=1, choices=ROLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "phone"]

    def __str__(self):
        return self.email
