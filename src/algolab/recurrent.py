def _validate(value: int, degree: int) -> None:
    if type(value) is not int or type(degree) is not int:
        raise TypeError("Основание и показатель должны быть целыми числами")
    if degree < 0:
        raise ValueError("Показатель должен быть неотрицательным")


def iter(value: int, degree: int) -> int:
    _validate(value, degree)
    result = 1
    while degree > 0:
        if degree % 2:
            result *= value
        value *= value
        degree //= 2
    return result


def recur(value: int, degree: int) -> int:
    _validate(value, degree)
    if degree == 0:
        return 1
    if degree % 2 == 0:
        return recur(value * value, degree // 2)
    return recur(value, degree - 1) * value


def recurrent(method: str, value: int, degree: int) -> int:
    if method == "--iter":
        return iter(value, degree)
    if method == "--recur":
        return recur(value, degree)
    raise ValueError(f"Неизвестный метод {method!r}")
