from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from referrals.models import ReferralBase
from referrals.utils import invite_code_valid


def invite_code_activation(request):
    """
    Активирует указанный код приглашения для текущего пользователя.
    Возвращает True, если код приглашения успешно активирован, иначе False.
    """
    invite_code = request.POST.get('invite_code')
    if not invite_code_valid(invite_code):
        return False
    query_set = ReferralBase.objects.filter(user_id=request.user.id)
    if not query_set:
        return False
    obj = query_set[0]
    if obj.self_invite_code == invite_code or obj.activated_invite_code:
        return False
    else:
        obj.activated_invite_code = invite_code
        obj.save()
        return True


def invite_code_activation_view(request):
    """
    UI-представление для активации кода приглашения.
    Перенаправляет на страницу профиля с указанием сообщения, если код введён неверно.
    """
    if request.method == 'POST':
        if not invite_code_activation(request):
            messages.error(request, 'Неверно введён код приглашения')
        return redirect('profile')


def api_invite_code_activation(request):
    """
    Возвращает JSON-ответ с результатом активации.
    API-представление для активации кода приглашения.
    """
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Пользователь не авторизирован'}, status=401)
        if invite_code_activation(request):
            return JsonResponse({'message': 'Код приглашения успешно активирован'})
        else:
            return JsonResponse({'message': 'Неверно введён код приглашения,или у данного пользователя код приглашения уже активирован'}, status=400)
