from django.http import JsonResponse
from django.shortcuts import render, redirect

from referrals.models import ReferralBase


def profile(request):
    """
    Получает данные о пользователе из модели ReferralBase (таблица реферальной системы).
    Returns:
        Возвращает кортеж, содержащий:
        tuple:
        - self_invite_code (str): код приглашения текущего пользователя;
        - activated_invite_code (str): код приглашения, который активировал текущий пользователь;
        - invited_users (list): Список номеров телефонов пользователей, активировавших код текущего пользователя.
    """
    self_invite_code, activated_invite_code = ReferralBase.objects.filter(user_id=request.user.id).values_list(
        'self_invite_code', 'activated_invite_code')[0]
    invited_users = list(ReferralBase.objects.filter(activated_invite_code=self_invite_code).select_related('user').
                         values_list('user__phone_number', flat=True))

    return self_invite_code, activated_invite_code, invited_users


def profile_view(request):
    """
    UI-представление для отображения профиля пользователя.
    Если пользователь не авторизован, перенаправляет на страницу ввода номера телефона.
    Если пользователь авторизован, возвращает HTML-страницу профиля с данными пользователя.
    """
    if not request.user.is_authenticated:
        return redirect('authentication_number_input')
    self_invite_code, activated_invite_code, invited_users = profile(request)
    return render(request, 'accounts/profile.html', locals())


def api_profile(request):
    """
    API-представление для получения данных профиля пользователя.
    Возвращает JSON-ответ с ошибкой, если пользователь не авторизован.
    Если пользователь авторизован, возвращает JSON с данными профиля:
    - user_id (int): ID пользователя;
    - user_phone_number (str): номер телефона пользователя;
    - self_invite_code (str): код приглашения текущего пользователя;
    - activated_invite_code (str): код приглашения, который активировал текущий пользователь;
    - invited_users (list): Список номеров телефонов пользователей, активировавших код текущего пользователя.
    """
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Пользователь не авторизирован'}, status=401)
    self_invite_code, activated_invite_code, invited_users = profile(request)
    return JsonResponse({'user_id': request.user.id,
                         'user_phone_number': request.user.phone_number,
                         'self_invite_code': self_invite_code,
                         'activated_invite_code': activated_invite_code,
                         'invited_users': invited_users,
                         })
