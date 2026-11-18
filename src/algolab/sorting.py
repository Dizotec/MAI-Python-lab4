
from typing import Any


def _check_list(els: list[Any]) -> None:
    if not isinstance(els, list):
        raise TypeError("Ожидается список")


def quadratic(els: list[Any], *, reverse: bool = False) -> list[Any]:
    _check_list(els)
    result = els.copy()
    for end in range(len(result) - 1, 0, -1):
        for j in range(end):
            left, right = result[j], result[j + 1]
            swap = left < right if reverse else right < left
            if swap:
                result[j], result[j + 1] = right, left
    return result


def merge(left: list[Any], right: list[Any], *, reverse: bool = False) -> list[Any]:
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        take_right = left[i] < right[j] if reverse else right[j] < left[i]
        if take_right:
            result.append(right[j])
            j += 1
        else:
            result.append(left[i])
            i += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def effective(els: list[Any], *, reverse: bool = False) -> list[Any]:
    _check_list(els)
    if len(els) < 2:
        return els.copy()
    mid = len(els) // 2
    left = effective(els[:mid], reverse=reverse)
    right = effective(els[mid:], reverse=reverse)
    return merge(left, right, reverse=reverse)


def sorting(method: str, els: list[Any], *, reverse: bool = False) -> list[Any]:
    if method == "--quadratic":
        return quadratic(els, reverse=reverse)
    if method == "--effective":
        return effective(els, reverse=reverse)
    raise ValueError(f"Неизвестный метод сортировки {method!r}")
