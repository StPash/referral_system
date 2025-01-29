from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class SMSAuthenticationBackend(BaseBackend):
    """
    Кастомный бэкенд аутентификации с помощью одноразового пароля
    """
    def authenticate(self, request, otp=None):
        if not otp == str(request.session.get('otp')):
            return None
        user, created = User.objects.get_or_create(phone_number=request.session.get('phone_number'))
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

