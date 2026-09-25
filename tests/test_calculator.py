"""Тесты калькулятора"""

import pytest

from toolkit.calculator import calculate, validate, tokenize
from toolkit.errors import ToolkitErrors


def test_tokenize_space() -> None:
    """Проверка попадания пробелов"""
    assert tokenize(" 12.5 +\t-3 / 2") == ["12.5", "+", "-", "3", "/", "2"]


def test_validate_signed_numbers() -> None:
    """Проверка унарных знаков"""
    assert validate(["-", "2", "*", "+", "2"]) == ([-2.0, 2.0], ["*"])


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("2 + 3 * 4", 14.0),
        ("20 - 12 / 3 * 2 + 1", 13.0),
        ("8 / 4 / 2", 1.0),
        ("10 - 3 - 2", 5.0),
        ("2.5 * 4 + .5", 10.5),
        ("5. / 2", 2.5),
        ("-2 * -3", 6.0),
        ("2--3", 5.0),
        ("2+-3", -1.0),
        ("2++3", 5.0),
        ("+7", 7.0),
        (" 2 * - 3 ", -6.0),
        ("0", 0.0),
    ],
)


def test_calculate_valid_expression(expression: str, expected: float) -> None:
    """Учитывание приоритет, порядок, унарные знаки"""
    assert calculate(expression) == pytest.approx(expected)


@pytest.mark.parametrize("expression", ["", " ", "\t\n"])
def test_empty_expression(expression: str) -> None:
    """Пустое выражение"""
    with pytest.raises(ToolkitErrors, match="Пустое выражение"):
        calculate(expression)


def test_space_does_not_join_numbers() -> None:
    """Два числа через пробел не превращаются в одно число."""
    with pytest.raises(ToolkitErrors, match="Пропущен оператор"):
        calculate("12 34")


@pytest.mark.parametrize("expression", [".", "2..3", "1.2.3 + 4"])
def test_invalid_number(expression: str) -> None:
    """Проверка на неверную запись дроби"""
    with pytest.raises(ToolkitErrors, match="числовое значение"):
        calculate(expression)


@pytest.mark.parametrize("expression", ["1/0", "2/-0.0"])
def test_division_by_zero(expression: str) -> None:
    """Деление на ноль"""
    with pytest.raises(ToolkitErrors, match="Деление на ноль"):
        calculate(expression)


@pytest.mark.parametrize("expression", ["2 & 3", "abc", "2%3"])
def test_invalid_character(expression: str) -> None:
    """Проверка на другие символы"""
    with pytest.raises(ToolkitErrors, match="Недопустимый символ"):
        calculate(expression)


def test_too_large_number() -> None:
    """Проверка на переполнение"""
    with pytest.raises(ToolkitErrors, match="Результат слишком большой"):
        calculate("9" * 400)
