import argparse
import sys

from toolkit.calculator import calculate
from toolkit.errors import ToolkitErrors


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


def main(arg: list[str] | None = None) -> int:
    """..."""
    arguments = list(sys.argv[1:] if arg is None else arg)

    if len(arguments) == 2 and arguments[0] == "calc" and arguments[1] not in ('-h', '--help'):
        arguments.insert(1, "--")
    args = create_parser().parse_args(arguments)
    try:
        if args.command == "calc":
            result = calculate(args.expression)
        # else:
        #     # result = convert()
    except ToolkitErrors as e:
        print(e)
        return 2
    print(result)
    return 0
