from django.db import IntegrityError, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import CustomUser
from referrals.models import ReferralBase
from referrals.utils import generate_invite_code


@receiver(post_save, sender=CustomUser)
def create_user(sender, instance, created,  **kwargs):
    """
    Сигнал, который срабатывает после сохранения объекта CustomUser.
    При создании пользователя генерирует уникальный код приглашения
    и создает запись ReferralBase для этого пользователя.
    """
    if created:
        flag = True
        while flag:
            invite_code = generate_invite_code()
            try:
                ReferralBase.objects.create(user=instance, self_invite_code=invite_code, activated_invite_code=None)
                flag = False
            except IntegrityError:
                continue

