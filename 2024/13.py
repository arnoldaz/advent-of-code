from itertools import groupby
from typing import NamedTuple

from utils.string import get_ints

class Equation(NamedTuple):
    a1: int
    a2: int
    b1: int
    b2: int
    c1: int
    c2: int

    def solve(self) -> tuple[int, int]:
        # Solving using Cramer's Rule
        det_a = self.a1 * self.b2 - self.b1 * self.a2
        det_ax = self.c1 * self.b2 - self.b1 * self.c2
        det_ay = self.a1 * self.c2 - self.c1 * self.a2

        x, rem_x = divmod(det_ax, det_a)
        y, rem_y = divmod(det_ay, det_a)

        return (x, y) if rem_x == 0 and rem_y == 0 else (-1, -1)

def parse_input(lines: list[str], gold=False) -> list[Equation]:
    equations: list[Equation] = []
    machines = [
        [tuple[int, int](get_ints(line)) for line in group]
        for key, group in groupby(lines, key=bool)
        if key
    ]

    for button_a, button_b, prize in machines:
        (a1, a2), (b1, b2), (c1, c2) = button_a, button_b, prize
        equations.append(Equation(a1, a2, b1, b2, c1 + 10000000000000 if gold else c1, c2 + 10000000000000 if gold else c2))

    return equations

def silver_solution(lines: list[str]) -> int:
    equations = parse_input(lines)

    result = 0
    for equation in equations:
        x, y = equation.solve()
        if x > 0 and y > 0:
            result += x * 3 + y

    return result

def gold_solution(lines: list[str]) -> int:
    equations = parse_input(lines, True)

    result = 0
    for equation in equations:
        x, y = equation.solve()
        if x > 0 and y > 0:
            result += x * 3 + y

    return result
