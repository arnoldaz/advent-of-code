import re

def silver_solution(lines: list[str]) -> int:
    row, column = (int(x) for x in re.findall(r"\d+", lines[0]))

    n = (row + column - 1) * (row + column) // 2 - (row - 1)

    start = 252533
    multiply_by = 20151125
    divide_by = 33554393

    exponent = pow(start, n - 1, divide_by)
    return (multiply_by * exponent) % divide_by

def gold_solution(_lines: list[str]) -> int:
    return 0
