import random
import string

CHARS = string.ascii_letters + string.digits


def generate_invite_code():
    """
    Генерирует случайный 6-значный код
    """
    code = ''
    for _ in range(6):
        code += random.choice(CHARS)
    return code


def invite_code_valid(code):
    """
    Проверяет корректность введенного кода
    """
    if len(code) != 6:
        return False
    for el in code:
        if el not in CHARS:
            return False
    return True
