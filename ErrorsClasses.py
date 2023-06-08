"""
Собственные классы исключений
"""

class WrongBetError(Exception):
    def __init__(self, message="Неверная ставка."):
        print(message)


class ChipsCountError(Exception):
    def __init__(self, message="Неверная инициализация числа фишек."):
        print(message)


class WrongInputError(Exception):
    def __init__(self, message="Неверный ввод."):
        print(message)
