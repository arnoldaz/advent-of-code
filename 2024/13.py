import re
from typing import NamedTuple
import sympy as sp
from sympy.solvers import solve
from sympy import Symbol

# TODO

class Equation(NamedTuple):
    a_x: int
    a_y: int
    b_x: int
    b_y: int
    result_x: int
    result_y: int

def parse_input(lines: list[str], gold=False) -> list[Equation]:
    button_a_regex = r"Button A: X\+(\d+), Y\+(\d+)"
    button_b_regex = r"Button B: X\+(\d+), Y\+(\d+)"
    prize_regex = r"Prize: X=(\d+), Y=(\d+)"

    equations: list[Equation] = []

    i = 0
    while i < len(lines) + 1:
        button_a_match = re.match(button_a_regex, lines[i])
        button_b_match = re.match(button_b_regex, lines[i+1])
        prize_match = re.match(prize_regex, lines[i+2])
        assert button_a_match and button_b_match and prize_match, "Regex match should always find data"

        a_x, a_y = int(button_a_match.group(1)), int(button_a_match.group(2))
        b_x, b_y = int(button_b_match.group(1)), int(button_b_match.group(2))
        result_x, result_y = int(prize_match.group(1)), int(prize_match.group(2))

        equations.append(
            Equation(
                a_x,
                a_y,
                b_x,
                b_y,
                result_x if not gold else result_x + 10000000000000,
                result_y if not gold else result_y + 10000000000000,
            )
        )

        i += 4

    return equations


def silver_solution(lines: list[str]) -> int:
    equations = parse_input(lines)

    result = 0

    for equation in equations:
        x = Symbol("x", integer=True)
        y = Symbol("y", integer=True)
        eq1 = sp.Eq(equation.a_x * x + equation.b_x * y, equation.result_x) # type: ignore reportOperatorIssue
        eq2 = sp.Eq(equation.a_y * x + equation.b_y * y, equation.result_y) # type: ignore reportOperatorIssue
        output = solve([ eq1, eq2 ])

        if not isinstance(output, list):
            x_value = output.get(x)
            y_value = output.get(y)
            # print(x_value, y_value)
            result += int(x_value) * 3 + int(y_value)
        
    return result

def gold_solution(lines: list[str]) -> int:
    equations = parse_input(lines, True)

    result = 0

    for equation in equations:
        x = Symbol("x", integer=True)
        y = Symbol("y", integer=True)
        eq1 = sp.Eq(equation.a_x * x + equation.b_x * y, equation.result_x) # type: ignore reportOperatorIssue
        eq2 = sp.Eq(equation.a_y * x + equation.b_y * y, equation.result_y) # type: ignore reportOperatorIssue
        output = solve([ eq1, eq2 ])

        if not isinstance(output, list):
            x_value = output.get(x)
            y_value = output.get(y)
            # print(x_value, y_value)
            result += int(x_value) * 3 + int(y_value)
        
    return result
