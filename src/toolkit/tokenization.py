"""Тут лежит все для токенизации"""

from toolkit.constants import OPERATORS, DIGITS
from toolkit.errors import ToolkitErrors


def tokenize(expression: str) -> list[str]:
    """Разделить строку на числа и операторы, пропуская пробелы."""
    tokens = []
    position = 0
    while position < len(expression):
        char = expression[position]
        if char.isspace():
            position += 1
        elif char in OPERATORS:
            tokens.append(char)
            position += 1
        elif char in DIGITS or char == ".":
            start = position
            while position < len(expression):
                char = expression[position]
                if char not in DIGITS and char != ".":
                    break
                position += 1
            tokens.append(expression[start:position])
        else:
            raise ToolkitErrors(f"Недопустимый символ: {char}")
    return tokens
