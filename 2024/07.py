from typing import NamedTuple

class Equation(NamedTuple):
    result: int
    numbers: list[int]

def parse_input(lines: list[str]) -> list[Equation]:
    equations: list[Equation] = []
    for line in lines:
        result_string, numbers_string = line.split(": ")
        result = int(result_string)
        numbers = [int(number) for number in numbers_string.split()]
        equations.append(Equation(result, numbers))

    return equations

def is_equation_possible(equation: Equation, include_concatenation: bool) -> bool:
    def check_possible_equations_dfs(current_result: int, equation: Equation, depth: int):
        if current_result == equation.result and len(equation.numbers) == depth:
            return True
        if depth >= len(equation.numbers) or current_result > equation.result:
            return False

        if check_possible_equations_dfs(current_result + equation.numbers[depth], equation, depth + 1):
            return True
        if check_possible_equations_dfs(current_result * equation.numbers[depth], equation, depth + 1):
            return True
        if include_concatenation and check_possible_equations_dfs(int(f"{current_result}{equation.numbers[depth]}"), equation, depth + 1):
            return True

        return False

    return check_possible_equations_dfs(equation.numbers[0], equation, 1)

def silver_solution(lines: list[str]) -> int:
    equations = parse_input(lines)
    return sum(equation.result for equation in equations if is_equation_possible(equation, False))

def gold_solution(lines: list[str]) -> int:
    equations = parse_input(lines)
    return sum(equation.result for equation in equations if is_equation_possible(equation, True))
