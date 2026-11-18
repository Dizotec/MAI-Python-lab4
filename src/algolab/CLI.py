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


def main() -> None:
    args = sys.argv[1:]
    parser = argparse.ArgumentParser(prog="algolab",usage="algolab {benchmark,recurrent,sorting,struct,generate} ...")
    if not args or args[0] in ("-h", "--help"):
        parser.print_help()
        return

    try:
        if args[0] == "benchmark":
            if len(args) < 2:
                parser.error("Укажи sorting или recurrent")
            if args[1] == "sorting":
                if args[2:3] == ["--quadratic"]:
                    print(benchmark_sort_quad(args[3:]))
                elif args[2:3] == ["--effective"]:
                    print(benchmark_sort_effect(args[3:]))
                else:
                    report = argparse.ArgumentParser(prog="algolab benchmark sorting")
                    report.add_argument("--sizes", type=int, nargs="+", default=SIZES)
                    report.add_argument("--seed", type=int, default=42)
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
            gen = argparse.ArgumentParser(prog="algolab generate")
            gen.add_argument("--kind", choices=KINDS, required=True)
            gen.add_argument("--size", type=int, required=True)
            gen.add_argument("--seed", type=int, default=None)
            options = gen.parse_args(args[1:])
            print(generate(options.kind, options.size, options.seed))
        else:
            parser.error("Неизвестная команда")
    except (TypeError, ValueError) as error:
        parser.error(str(error))
