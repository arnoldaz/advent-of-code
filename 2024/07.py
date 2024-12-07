from enum import Enum
from typing import NamedTuple

class Equation(NamedTuple):
    result: int
    numbers: list[int]

class Operation(Enum):
    ADD = 1
    MULT = 2
    CONC = 3

def parse_input(lines: list[str]) -> list[Equation]:
    equations: list[Equation] = []
    for line in lines:
        result_string, numbers_string = line.split(": ")
        numbers = [int(number) for number in numbers_string.split()]
        equations.append(Equation(int(result_string), numbers))

    return equations

def check_equation_possible(equation: Equation, allowed_operations: list[Operation], operations: list[Operation]) -> bool:
    # print(f"recursion start", operations, len(equation.numbers))
    operator_amount = len(equation.numbers) - 1
    if len(operations) != operator_amount:
        return any(check_equation_possible(equation, allowed_operations, operations + [new_operation]) for new_operation in allowed_operations)

    ongoing_result = equation.numbers[0]
    for i in range(1, len(equation.numbers)):
        operation = operations[i-1]
        number = equation.numbers[i]
        # print(f"START: {ongoing_result}, OP: {operation}, NUM: {number}")
        match operation:
            case Operation.ADD:
                ongoing_result += number
            case Operation.MULT:
                ongoing_result *= number
            case Operation.CONC:
                ongoing_result = int(str(ongoing_result) + str(number))
        # print(f"END: {ongoing_result}")

    return ongoing_result == equation.result

def silver_solution(lines: list[str]) -> int:
    equations = parse_input(lines)
    return sum(equation.result for equation in equations if check_equation_possible(equation, [Operation.ADD, Operation.MULT], []))

def gold_solution(lines: list[str]) -> int: # runs for ~25s
    equations = parse_input(lines)
    return sum(equation.result for equation in equations if check_equation_possible(equation, [Operation.ADD, Operation.MULT, Operation.CONC], []))