import math

from toolkit.constants import OPERATORS
from toolkit.errors import ToolkitErrors


def validate(tokens: list[str]) -> tuple[list[float], list[str]]:
    """Проверка порядка токенов и сбор числа"""

    if not tokens:
        raise ToolkitErrors("Пустое выражение.")

    numbers = []
    operation = []
    position = 0
    while position < len(tokens):
        sign = 1
        while position < len(tokens) and tokens[position] in ("+", "-"):
            if tokens[position] == "-":
                sign *= -1
            position += 1
        if position == len(tokens):
            raise ToolkitErrors("Пропущен операнд")
        if tokens[position] in OPERATORS:
            raise ToolkitErrors("Указаны лишние операторы")
        try:
            number = float(tokens[position]) * sign
        except ValueError as error:
            raise ToolkitErrors("Неверное числовое значение") from error
        if not math.isfinite(number):
            raise ToolkitErrors("Число должно быть конечны")
        numbers.append(number)
        position += 1

        if position < len(tokens):
            if tokens[position] not in OPERATORS:
                raise ToolkitErrors("Пропущен оператор")
            operation.append(tokens[position])
            position += 1
            if position == len(tokens):
                raise ToolkitErrors("После оператора пропущен операнд")
    return numbers, operation
