import argparse
# import sys


def create_parser() -> argparse.ArgumentParser:
    """..."""
    parser = argparse.ArgumentParser(description="Калькулятор и конвертер")
    commands = parser.add_subparsers(dest="command", required=True)

    calc_parser = commands.add_parser("calc", help="Вычисление")
    calc_parser.add_argument("expression", help="Выражение в кавычках")

    convert_parser = commands.add_parser("convert", help="Перевод")
    convert_parser.add_argument("value", help="Число")
    convert_parser.add_argument("--from", dest="from_unit", required=True)
    convert_parser.add_argument("--to", dest="to_unit", required=True)
    return parser
