from typing import Optional


def year_over_year(series: list[tuple[int, Optional[float]]], unit: str) -> list[tuple[int, Optional[float]]]:
    result: list[tuple[int, Optional[float]]] = [(series[0][0], None)]
    for i in range(1, len(series)):
        year, val = series[i]
        _, prev = series[i - 1]
        if prev is None or prev == 0 or val is None:
            result.append((year, None))
        else:
            if unit == "%":
                result.append((year, round(val - prev, 2)))
            else:
                result.append((year, round(((val - prev) / prev) * 100, 2)))
    return result


def cagr(series: list[tuple[int, Optional[float]]]) -> Optional[float]:
    non_null = [(y, v) for y, v in series if v is not None]
    if len(non_null) < 2:
        return None
    first_year, first_val = non_null[0]
    last_year, last_val = non_null[-1]
    if first_val is None or last_val is None or first_val <= 0 or last_val <= 0:
        return None
    n = last_year - first_year
    if n <= 0:
        return None
    result = ((last_val / first_val) ** (1 / n) - 1) * 100
    return round(result, 2)


def normalize_to_base(
    series: list[tuple[int, Optional[float]]], base_year: int
) -> list[tuple[int, Optional[float]]]:
    base_val = None
    for y, v in series:
        if y == base_year:
            base_val = v
            break
    if base_val is None or base_val == 0:
        return [(y, None) for y, _ in series]
    return [
        (y, round((v / base_val) * 100, 2) if v is not None else None)
        for y, v in series
    ]
