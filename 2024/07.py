from enum import Enum
from functools import cache
from typing import NamedTuple
from itertools import combinations, product, permutations

# TODO

class Equation(NamedTuple):
    result: int
    numbers: tuple[int, ...]

class Operation(Enum):
    ADD = 1
    MULT = 2
    CONC = 3

def parse_input(lines: list[str]) -> list[Equation]:
    equations: list[Equation] = []
    for line in lines:
        result_string, numbers_string = line.split(": ")
        numbers = tuple(int(number) for number in numbers_string.split())
        equations.append(Equation(int(result_string), numbers))

    return equations

allowed_operations: list[Operation] = []

@cache
def check_equation_possible(equation: Equation, operations: tuple[Operation, ...]) -> bool:
    # print(equation.result, equation.numbers, operations)
    # print(f"recursion start", operations, len(equation.numbers))
    operator_amount = len(equation.numbers) - 1
    if len(operations) != operator_amount:
        return any(check_equation_possible(equation, operations + (new_operation,)) for new_operation in allowed_operations)

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
        if ongoing_result > equation.result:
            return False

    return ongoing_result == equation.result

# def test(num1, num2):
#     return int(str(num1) + str(num2))

def is_equation_possible(equation: Equation):
    # print(f"recursion start", operations, len(equation.numbers))
    operator_amount = len(equation.numbers) - 1
    permutations = product(range(3), repeat=operator_amount)

    # print(list(permutations))

    for permutation in permutations:
        ongoing_result = equation.numbers[0]
        for i in range(1, len(equation.numbers)):
            operation = permutation[i-1]
            number = equation.numbers[i]
            # print(f"START: {ongoing_result}, OP: {operation}, NUM: {number}")
            match operation:
                case 0:
                    ongoing_result += number
                case 1:
                    ongoing_result *= number
                case 2:
                    ongoing_result = int(str(ongoing_result) + str(number))
                    # int(str(ongoing_result) + str(number))
            # print(f"END: {ongoing_result}")
            if ongoing_result > equation.result:
                break

        if ongoing_result == equation.result:
            return True

    return False

def dfs(current_result: int, equation: Equation, depth: int):
    # print("   " * depth, current_result, depth)
    if current_result == equation.result and len(equation.numbers) == depth:
        return True
    if depth >= len(equation.numbers) or current_result > equation.result:
        return False

    # print("   " * depth, "sum")
    if dfs(current_result + equation.numbers[depth], equation, depth + 1):
        return True
    # print("   " * depth, "mult")
    if dfs(current_result * equation.numbers[depth], equation, depth + 1):
        return True
    # print("   " * depth, "coc")
    # if dfs(int(str(current_result) + str(equation.numbers[depth])), equation, depth + 1):
    if dfs(int(f'{current_result}{equation.numbers[depth]}'), equation, depth + 1):
        return True

    return False

def dfs_iterative(equation: Equation):
    stack = [(equation.numbers[0], 1)]  

    while stack:
        current_result, depth = stack.pop()

        # Check if we've found a valid solution
        if current_result == equation.result and len(equation.numbers) == depth:
            return True

        # Skip invalid states
        if depth >= len(equation.numbers) or current_result > equation.result:
            continue

        # Push next states to the stack
        stack.append((current_result + equation.numbers[depth], depth + 1))  # Sum
        stack.append((current_result * equation.numbers[depth], depth + 1))  # Multiplication
        stack.append((int(f'{current_result}{equation.numbers[depth]}'), depth + 1))  # Concatenation

    return False

def silver_solution(lines: list[str]) -> int:
    return 1
    equations = parse_input(lines)
    return sum(equation.result for equation in equations if check_equation_possible(equation, [Operation.ADD, Operation.MULT], []))

def gold_solution(lines: list[str]) -> int: # runs for ~25s
    # global allowed_operations
    equations = parse_input(lines)
    # equations = [equations[2]]

    # allowed_operations = [Operation.ADD, Operation.MULT, Operation.CONC]

    # equations = [Equation(76, (2,4,6,21,9))]

    result = 0
    for equation in equations:
        # Equation(result=76, numbers=(2, 4, 6, 21, 9)) 
        # print(equation)
        # a = is_equation_possible(equation)
        # b = dfs(1, equation, equation.numbers[0])
        # print("possible", equation, a, b, "ERROR!!!!!!!!!!!!!!!!!!!ERROR!!!!!!!!!!!!!!!!!!!ERROR!!!!!!!!!!!!!!!!!!!ERROR!!!!!!!!!!!!!!!!!!!ERROR!!!!!!!!!!!!!!!!!!!" if a != b else "")
        # if is_equation_possible(equation):
        if dfs(equation.numbers[0], equation, 1):
        # if dfs_iterative(equation):
            result += equation.result

    return result

    # # y = list(x)
    # # print(y)

    return sum(equation.result for equation in equations if check_equation_possible(equation, [Operation.ADD, Operation.MULT, Operation.CONC], []))