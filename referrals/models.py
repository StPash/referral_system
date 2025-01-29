from django.db import models

from accounts.models import CustomUser


class ReferralBase(models.Model):
    """
    Модель для хранения данных о реферальной системе.
    Поля:
    user (OneToOneField): связь с моделью CustomUser. Может быть пустым;
    self_invite_code (CharField): уникальный код приглашения пользователя, генерируется автоматически при регистрации;
    activated_invite_code (CharField): код приглашения, который активировал пользователь. Может быть пустым.
    """
    user = models.OneToOneField(CustomUser, on_delete=models.SET_NULL, blank=True, null=True)
    self_invite_code = models.CharField(max_length=6, unique=True)
    activated_invite_code = models.CharField(max_length=6, default='', blank=True, null=True)
