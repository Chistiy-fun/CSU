"""Проверки конвертера"""

import pytest

from toolkit.converter import convert
from toolkit.errors import ToolkitErrors


@pytest.mark.parametrize(
    ("value", "from_unit", "to_unit", "expected"),
    [
        (1, "km", "m", 1000.0),
        (1000, "mm", "m", 1.0),
        (2, "m", "cm", 200.0),
        (25, "cm", "mm", 250.0),
        (1, "kg", "g", 1000.0),
        (500, "g", "kg", 0.5),
        (2, "KM", "Cm", 200000.0),
        (0, "c", "f", 32.0),
        (32, "f", "c", 0.0),
        (0, "c", "k", 273.15),
        (273.15, "k", "c", 0.0),
        (32, "f", "k", 273.15),
        (273.15, "k", "f", 32.0),
        (-40, "c", "f", -40.0),
        (-273.15, "c", "k", 0.0),
        (-459.67, "f", "k", 0.0),
        (0, "k", "f", -459.67),
        (0, "k", "k", 0.0),
    ],
)
def test_unit_conversion(
    value: float, from_unit: str, to_unit: str, expected: float
) -> None:
    """Все группы, направления температуры и границы поддерживаются."""
    result = convert(value, from_unit, to_unit)
    assert isinstance(result, float)
    assert result == pytest.approx(expected)


def test_string_value() -> None:
    """Значение из CLI можно передать строкой."""
    assert convert("1.5", "kg", "g") == 1500.0


@pytest.mark.parametrize("unit", ["mm", "cm", "m", "km", "g", "kg", "c", "f", "k"])
def test_same_unit(unit: str) -> None:
    """При одинаковых единицах значение сохраняется."""
    assert convert(10, unit, unit) == 10.0


@pytest.mark.parametrize("from_unit,to_unit", [("x", "m"), ("m", "x")])
def test_unknown_unit(from_unit: str, to_unit: str) -> None:
    """Неизвестная исходная или конечная единица"""
    with pytest.raises(ToolkitErrors, match="Неизвестная единица"):
        convert(1, from_unit, to_unit)


@pytest.mark.parametrize("from_unit,to_unit", [("m", "kg"), ("c", "mm"), ("g", "k")])
def test_incompatible_units(from_unit: str, to_unit: str) -> None:
    """Разные группы нельзя преобразовать друг в друга."""
    with pytest.raises(ToolkitErrors, match="Несовместимые"):
        convert(1, from_unit, to_unit)


@pytest.mark.parametrize("value", ["hello", "", "1,5", "nan", "inf", "-inf"])
def test_invalid_conversion_value(value: str) -> None:
    """Нужны корректные числа"""
    with pytest.raises(ToolkitErrors):
        convert(value, "m", "cm")


@pytest.mark.parametrize("value,unit", [(-273.16, "c"), (-459.68, "f"), (-0.01, "k")])
def test_below_absolute_zero(value: float, unit: str) -> None:
    """Температура ниже границы"""
    with pytest.raises(ToolkitErrors, match="абсолютного нуля"):
        convert(value, unit, unit)


def test_conversion_overflow() -> None:
    """Слишком большой результат"""
    with pytest.raises(ToolkitErrors, match="слишком большой"):
        convert(1e308, "km", "mm")
