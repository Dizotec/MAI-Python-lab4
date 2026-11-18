from collections.abc import Callable, Sequence
from statistics import median
from time import perf_counter

from algolab.generators import KINDS, generate
from algolab.recurrent import iter as iterative_power
from algolab.recurrent import recur
from algolab.sorting import effective, quadratic

REPEATS = 5
SIZES = (100, 1000, 10000)


def _measure_power(function: Callable[[int, int], int], args: Sequence[str]) -> float:
    value, degree = map(int, args)
    times = []
    for _ in range(REPEATS):
        start = perf_counter()
        function(value, degree)
        times.append(perf_counter() - start)
    return median(times)


def benchmark_recurn_iter(args: Sequence[str]) -> float:
    return _measure_power(iterative_power, args)


def benchmark_recurn_recur(args: Sequence[str]) -> float:
    """Измеряет рекурсивную степень."""
    return _measure_power(recur, args)


def _measure_sort(function: Callable[[list[int]], list[int]], data: list[int]) -> float:
    times = []
    for _ in range(REPEATS):
        working_data = data.copy()
        start = perf_counter()
        function(working_data)
        times.append(perf_counter() - start)
    return median(times)


def benchmark_sort_quad(args: Sequence[str | int]) -> float:
    return _measure_sort(quadratic, [int(value) for value in args])


def benchmark_sort_effect(args: Sequence[str | int]) -> float:
    return _measure_sort(effective, [int(value) for value in args])


def sorting_report(sizes: Sequence[int] = SIZES, seed: int = 42) -> str:
    rows = [
        "| Тип входа | Размер | Пузырьковая, мс | Слиянием, мс |",
        "|---|---:|---:|---:|",
    ]
    for size in sizes:
        for kind in KINDS:
            data = generate(kind, size, seed)
            bubble_ms = 1000 * _measure_sort(quadratic, data)
            merge_ms = 1000 * _measure_sort(effective, data)
            rows.append(f"| {kind} | {size} | {bubble_ms:.3f} | {merge_ms:.3f} |")
    return "\n".join(rows)
