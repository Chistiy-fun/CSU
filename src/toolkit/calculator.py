"""Вычисления"""

import math
from toolkit.errors import ToolkitErrors
from toolkit.tokenization import tokenize
from toolkit.validation import validate


def calculate_values(numbers: list[float], operators: list[str]) -> float:
    """Вычислить проверенные данные, сначала выполняя умножение и деление."""
    total = 0.0
    term = numbers[0]
    for index, operator in enumerate(operators):
        number = numbers[index + 1]
        if operator == "*":
            term *= number
        elif operator == "/":
            if number == 0:
                raise ToolkitErrors("Деление на ноль")
            term /= number
        else:
            total += term
            term = number if operator == "+" else -number
        if not math.isfinite(term) or not math.isfinite(total):
            raise ToolkitErrors("Результат слишком большой")
    result = total + term
    if not math.isfinite(result):
        raise ToolkitErrors("Результат слишком большой")
    return result


def calculate(expression: str) -> float:
    """Вычислить выражение"""
    tokens = tokenize(expression)
    numbers, operators = validate(tokens)
    return calculate_values(numbers, operators)
