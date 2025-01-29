import random
import time

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import render, redirect

from authentication.utils import number_valid, otp_valid


def number_input(request):
    """
    Функция ввода и верификации номера телефона при авторизации пользователя.
    При корректном вводе номера телефона вызывает функцию имитирующую отправку смс кода generate_otp,
    сохраняет номер в сессии и возвращает True.
    Если номер телефона корректен возвращает False.
    """
    phone_number = request.POST.get('number')
    if phone_number and number_valid(phone_number):
        request.session['phone_number'] = phone_number

        return generate_otp(request)
    else:
        return False


def number_input_view(request):
    """
    UI-представление для ввода номера телефона.
    Возвращает HTML-страницу с формой ввода номера телефона и сообщением об ошибке, если номер введен неверно.
    """
    message = ''
    if request.method == 'POST':
        if number_input(request):
            return redirect('authentication_otp_input')
        else:
            message = 'Неверно указан номер, введите корректные данные'
    return render(request, 'authentication/number_input.html', {'message': message})


def api_number_input(request):
    """
    API-представление для ввода номера телефона.
    Возвращает JSON-ответ с сообщением об успешной отправке кода или ошибкой, если номер введен неверно.
    """
    if request.method == 'POST':
        if number_input(request):
            return JsonResponse({'message': f'Код отправлен на номер {request.session['phone_number']}',
                                 # Раскомментировать при необходимости отображения отправленного кода в JSON-ответе
                                 # 'otp': request.session['otp']
                                 })

        else:
            return JsonResponse({'error': 'Неверно указан номер'}, status=400)


def generate_otp(request):
    """
    Функция генерации одноразового пароля, имитации отправки и сохранения его в сессии для дальнейшей авторизации.
    Сгенерированный код отображается в консоли сервера
    """
    otp = random.randint(1000, 9999)
    request.session['otp'] = otp
    # Имитация отправки кода
    time.sleep(2)
    print(f"Отправленный код: {otp}")
    return True


def otp_input(request):
    """
    Функция ввода и верификации OTP.
    Возвращает True, если OTP корректен и пользователь успешно авторизован, иначе возвращает False.
    """
    otp = request.POST.get('otp')
    if otp and otp_valid(otp):
        user = authenticate(request, otp=otp)
        if user:
            login(request, user)
            request.session.pop('otp', None)
            request.session.pop('phone_number', None)
            return True
        else:
            return False
    else:
        return False


def otp_input_view(request):
    """
    UI-представление для ввода OTP.
    Возвращает HTML-страницу с формой ввода OTP и сообщением об ошибке, если код введен неверно.
    """
    message = ''
    if request.method == 'POST':
        if otp_input(request):
            return redirect('profile')
        else:
            message = 'Неверно указан код'
    return render(request, 'authentication/otp_input.html', {'message': message})


def api_otp_input(request):
    """
    API-представление для ввода OTP.
    Возвращает JSON-ответ с сообщением об успешной авторизации или ошибкой, если код введен неверно.
    """
    if request.method == 'POST':
        if otp_input(request):
            return JsonResponse({'message': f'Успешная авторизация пользователя',
                                 'user_id': request.user.id})
        else:
            return JsonResponse({'error': 'Неверно указан код'}, status=400)


def logout_view(request):
    """
    Представление для выхода пользователя из системы.
    Осуществляет выход из профиля пользователя и перенаправляет на страницу ввода номера телефона для авторизации.
    """
    logout(request)
    return redirect('authentication_number_input')

