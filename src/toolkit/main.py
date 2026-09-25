import argparse
import sys
import json

from toolkit.calculator import calculate
from toolkit.converter import convert
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
    """Вывод результата или ошибки"""
    arguments = list(sys.argv[1:] if arg is None else arg)

    if len(arguments) == 2 and arguments[0] == "calc" and arguments[1] not in ('-h', '--help'):
        arguments.insert(1, "--")
    args = create_parser().parse_args(arguments)
    try:
        if args.command == "calc":
            result = calculate(args.expression)
        else:
            result = convert(args.value, args.from_unit, args.to_unit)
    except ToolkitErrors as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return 2
    print(result)

    try:
        with open("successful_data.json", "r", encoding="utf-8") as f:
            content = f.read().strip()
            data = json.loads(content) if content else []
    except FileNotFoundError:
        data = []

    if arguments[0] == "convert":
        data.append({
            "argument": arguments[0],
            "expression": " ".join(arguments),
            "result": result,
        })
    else:
        data.append({
            "argument": arguments[0],
            "expression": arguments[2],
            "result": result,
        })

    with open("successful_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    return 0
