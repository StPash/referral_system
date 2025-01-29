from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


class CustomUser(AbstractBaseUser):
    """
    Модель пользователя.

    Attributes:
        phone_number (str): Номер телефона пользователя.
    """
    phone_number = models.CharField(max_length=10, unique=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone_number
