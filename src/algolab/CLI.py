import argparse
import sys

from algolab.benchmark import (
    SIZES,
    benchmark_recurn_iter,
    benchmark_recurn_recur,
    benchmark_sort_effect,
    benchmark_sort_quad,
    sorting_report,
)
from algolab.generators import KINDS, generate
from algolab.recurrent import recurrent
from algolab.sorting import sorting
from algolab.stack import demo_stack


def _make_parser(
    prog: str, description: str, *, usage: str | None = None, epilog: str | None = None
) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=prog,
        description=description,
        usage=usage,
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    if sys.version_info >= (3, 14):
        parser.color = False
    return parser


def _print_command_help(command: list[str]) -> None:
    prog = "python -m algolab " + " ".join(command)
    parser = _make_parser(prog, "")
    if command == ["sorting"]:
        parser.description = "Отсортировать список целых чисел."
        methods = parser.add_mutually_exclusive_group(required=True)
        methods.add_argument("--quadratic", action="store_true", help="Пузырьковая сортировка.")
        methods.add_argument("--effective", action="store_true", help="Сортировка слиянием.")
        parser.add_argument("--reverse", action="store_true", help="Сортировать по убыванию.")
        parser.add_argument("числа", nargs="*", help="Целые числа через пробел.")
    elif command in (["recurrent"], ["benchmark", "recurrent"]):
        benchmark_help = command[0] == "benchmark"
        parser.description = (
            "Измерить время вычисления степени. Без флага сравниваются оба метода."
            if benchmark_help else "Вычислить степень целого числа."
        )
        methods = parser.add_mutually_exclusive_group(required=not benchmark_help)
        methods.add_argument("--iter", action="store_true", help="Итеративный метод.")
        methods.add_argument("--recur", action="store_true", help="Рекурсивный метод.")
        nargs = "?" if benchmark_help else None
        parser.add_argument("основание", nargs=nargs, help="Целое число.")
        parser.add_argument("показатель", nargs=nargs, help="Целое число от 0.")
        if benchmark_help:
            parser.epilog = "Без аргументов команда сравнивает оба метода на 2 в степени 100."
    elif command == ["benchmark"]:
        parser.description = "Измерить время работы алгоритмов."
        parser.add_argument("группа", choices=("sorting", "recurrent"),
                            help="Сортировки или быстрая степень.")
        parser.epilog = "Справка по группе: python -m algolab benchmark sorting --help"
    elif command == ["struct"]:
        parser.description = "Показать добавление, просмотр и извлечение элементов стека."
    parser.print_help()


def main() -> None:
    args = sys.argv[1:]
    parser = _make_parser(
        "algolab",
        "Быстрая степень, сортировки, стек, генераторы и замеры времени.",
        usage="python -m algolab {benchmark,recurrent,sorting,struct,generate} ...",
        epilog=(
            "  recurrent  Вычислить степень\n"
            "  sorting    Отсортировать список целых чисел\n"
            "  struct     Показать работу стека\n"
            "  generate   Создать список для проверки сортировок\n"
            "  benchmark  Измерить время работы алгоритмов\n\n"
            "Справка по команде: python -m algolab sorting --help"
        ),
    )
    if not args or args[0] in ("-h", "--help"):
        parser.print_help()
        return

    wants_help = "-h" in args or "--help" in args
    if wants_help and args[0] in ("sorting", "recurrent", "struct"):
        _print_command_help(args[:1])
        return
    if wants_help and args[0] == "benchmark" and args[1] in ("-h", "--help", "recurrent"):
        _print_command_help(args[:2] if args[1] == "recurrent" else args[:1])
        return

    try:
        if args[0] == "benchmark":
            if len(args) < 2:
                parser.error("Укажи sorting или recurrent")
            if args[1] == "sorting":
                if not wants_help and args[2:3] == ["--quadratic"]:
                    print(benchmark_sort_quad(args[3:]))
                elif not wants_help and args[2:3] == ["--effective"]:
                    print(benchmark_sort_effect(args[3:]))
                else:
                    report = _make_parser(
                        "python -m algolab benchmark sorting",
                        "Сравнить время двух сортировок.",
                        epilog=(
                            "Замер на заданном списке\n"
                            "  python -m algolab benchmark sorting --quadratic ЧИСЛА...\n"
                            "  python -m algolab benchmark sorting --effective ЧИСЛА..."
                        ),
                    )
                    report.add_argument("--sizes", type=int, nargs="+", default=SIZES,
                                        help="Размеры списков. По умолчанию 100, 1000 и 10000.")
                    report.add_argument("--seed", type=int, default=42,
                                        help="Начальное значение генератора. По умолчанию 42.")
                    if wants_help:
                        report.print_help()
                        return
                    options = report.parse_args(args[2:])
                    print(sorting_report(options.sizes, options.seed))
            elif args[1] == "recurrent":
                if args[2:3] == ["--iter"]:
                    print(benchmark_recurn_iter(args[3:]))
                elif args[2:3] == ["--recur"]:
                    print(benchmark_recurn_recur(args[3:]))
                else:
                    values = args[2:] or ["2", "100"]
                    print(f"Итеративная, с: {benchmark_recurn_iter(values):.9f}")
                    print(f"Рекурсивная, с: {benchmark_recurn_recur(values):.9f}")
            else:
                parser.error("Неизвестная группа benchmark")
        elif args[0] == "recurrent":
            if len(args) != 4:
                parser.error("Укажи метод, основание и показатель")
            print(recurrent(args[1], int(args[2]), int(args[3])))
        elif args[0] == "sorting":
            if len(args) < 2:
                parser.error("Укажи --quadratic или --effective")
            reverse = "--reverse" in args[2:]
            els = [int(value) for value in args[2:] if value != "--reverse"]
            print(sorting(args[1], els, reverse=reverse))
        elif args[0] == "struct":
            demo_stack()
        elif args[0] == "generate":
            gen = _make_parser("python -m algolab generate", "Создать список для проверки сортировок.")
            gen.add_argument("--kind", choices=KINDS, required=True, metavar="ТИП",
                             help="Тип списка. Варианты: " + ", ".join(KINDS) + ".")
            gen.add_argument("--size", type=int, required=True, metavar="N",
                             help="Количество элементов в списке.")
            gen.add_argument("--seed", type=int, default=None, metavar="N",
                             help="Целое число для воспроизведения случайного списка.")
            options = gen.parse_args(args[1:])
            print(generate(options.kind, options.size, options.seed))
        else:
            parser.error("Неизвестная команда")
    except (TypeError, ValueError) as error:
        parser.error(str(error))
