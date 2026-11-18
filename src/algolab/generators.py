
import random

KINDS = ("random", "sorted", "reverse", "almost-sorted", "duplicates")


def _check_size(size: int) -> None:
    if type(size) is not int:
        raise TypeError("Размер должен быть целым числом")
    if size < 0:
        raise ValueError("Размер должен быть неотрицательным")


def rand_gener(size: int, seed: int | None = None) -> list[int]:
    _check_size(size)
    rng = random.Random(seed)
    return [rng.randint(-1000, 1000) for _ in range(size)]


def sorted_gener(size: int) -> list[int]:
    _check_size(size)
    return list(range(size))


def reverse_gener(size: int) -> list[int]:
    _check_size(size)
    return list(range(size - 1, -1, -1))


def almost_sorted_gener(size: int, seed: int | None = None) -> list[int]:
    result = sorted_gener(size)
    if size >= 2:
        rng = random.Random(seed)
        for i in rng.sample(range(0, size - 1, 2), max(1, size // 20)):
            result[i], result[i + 1] = result[i + 1], result[i]
    return result


def duplicates_gener(size: int, seed: int | None = None) -> list[int]:
    _check_size(size)
    rng = random.Random(seed)
    return [rng.randint(0, 4) for _ in range(size)]


def generate(kind: str, size: int, seed: int | None = None) -> list[int]:
    if kind == "random":
        return rand_gener(size, seed)
    if kind == "sorted":
        return sorted_gener(size)
    if kind == "reverse":
        return reverse_gener(size)
    if kind == "almost-sorted":
        return almost_sorted_gener(size, seed)
    if kind == "duplicates":
        return duplicates_gener(size, seed)
    raise ValueError(f"Неизвестный тип набора {kind!r}")
