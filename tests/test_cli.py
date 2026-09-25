"""Запуск настоящего CLI и проверка потоков и кодов завершения."""

import subprocess
import sys

import pytest


def run_cli(*arguments: str) -> subprocess.CompletedProcess[str]:
    """Запустить установленный пакет"""
    return subprocess.run(
        [sys.executable, "-m", "toolkit", *arguments],
        capture_output=True,
        text=True,
        check=False,
    )


@pytest.mark.parametrize(
    "arguments,expected",
    [
        (["calc", "2+3*4"], 14.0),
        (["calc", "-2+3"], 1.0),
        (["convert", "1.5", "--from", "kg", "--to", "g"], 1500.0),
        (["convert", "-40", "--from", "c", "--to", "f"], -40.0),
    ],
)
def test_cli_success(arguments: list[str], expected: float) -> None:
    """Успешная команда выводит число и возвращает ноль."""
    result = run_cli(*arguments)
    assert result.returncode == 0
    assert float(result.stdout.strip()) == pytest.approx(expected)
    assert result.stderr == ""


@pytest.mark.parametrize(
    "arguments",
    [
        ["calc", "1/0"],
        ["calc", ""],
        ["calc", "2*/3"],
        ["convert", "abc", "--from", "m", "--to", "cm"],
        ["convert", "1", "--from", "m", "--to", "kg"],
        ["convert", "-1", "--from", "k", "--to", "c"],
        ["convert", "1", "--from", "unknown", "--to", "m"],
        ["convert", "1", "--from", "m"],
        ["calc"],
        [],
    ],
)
def test_cli_error(arguments: list[str]) -> None:
    """Ошибка попадает только в stderr, код завершения 2."""
    result = run_cli(*arguments)
    assert result.returncode == 2
    assert result.stdout == ""
    assert result.stderr.strip()
    assert "Traceback" not in result.stderr


@pytest.mark.parametrize(
    "arguments", [["--help"], ["calc", "--help"], ["convert", "--help"]]
)
def test_cli_help(arguments: list[str]) -> None:
    """Справка доступна для пакета и обеих команд."""
    result = run_cli(*arguments)
    assert result.returncode == 0
    assert result.stdout.strip()
    assert result.stderr == ""
