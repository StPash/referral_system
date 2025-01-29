def number_valid(number):
    """
    Проверяет корректность введенного номера телефона
    """
    return number.isdigit() and len(number) == 10


def otp_valid(otp):
    """
    Проверяет корректность введенного одноразового пароля
    """
    return otp.isdigit() and len(otp) == 4
