"""Конвертация тут должна быть"""
import math

from toolkit.constants import (ABSOLUTE_ZERO,
                               FAHRENHEIT_SCALE,
                               FAHRENHEIT_OFFSET,
                               LENGTH_FACTORS,
                               MASS_FACTORS,)
from toolkit.errors import ToolkitErrors


def get_group(unit: str) -> str:
    """Нахождение группы единиц измерения"""
    if unit in LENGTH_FACTORS:
        return "length"
    if unit in MASS_FACTORS:
        return "mass"
    if unit in ABSOLUTE_ZERO:
        return "temperature"
    raise ToolkitErrors(f"Неизвестная единица: {unit}")


def convert_temperature(value: float, from_unit:str, to_unit: str) -> float:
    """Перевод температуры"""
    if value < ABSOLUTE_ZERO[from_unit]:
        raise ToolkitErrors("Температура ниже абсолютного нуля")
    if from_unit == to_unit:
        return value

    if from_unit == "c":
        celsius = value
    elif from_unit == "f":
        celsius = (value - FAHRENHEIT_OFFSET) * FAHRENHEIT_SCALE
    else:
        celsius = value + ABSOLUTE_ZERO["c"]

    if to_unit == "c":
        return celsius
    elif to_unit == "f":
        return celsius / FAHRENHEIT_SCALE + FAHRENHEIT_OFFSET
    return celsius - ABSOLUTE_ZERO["c"]


def convert_mass(value: float, from_unit: str, to_unit: str) -> float:
    factors = LENGTH_FACTORS if get_group(from_unit) == "length" else MASS_FACTORS
    result = value * (factors[from_unit] / factors[to_unit])
    return result


def convert(value: str | float, from_unit: str, to_unit: str) -> float:
    """Перевод чисел между единицами различных групп"""
    try:
        number = float(value)
    except ValueError:
        raise ToolkitErrors("Неверное числовое значение")

    if not math.isfinite(number):
        raise ToolkitErrors("Число должно быть конечным")

    from_unit = from_unit.lower()
    to_unit = to_unit.lower()
    from_group = get_group(from_unit)
    to_group = get_group(to_unit)

    if from_group != to_group:
        raise ToolkitErrors("Несовместимые единицы измерения")

    if from_group == "temperature":
        result = convert_temperature(number, from_unit, to_unit)
    else:
        result = convert_mass(number, from_unit, to_unit)

    if not math.isfinite(result):
        raise ToolkitErrors("Результат слишком большой")

    return result
