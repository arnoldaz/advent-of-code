import math
from utils.grid import Grid

def perform_operation(numbers: list[int], operation: str) -> int:
    match operation:
        case "+":
            return sum(numbers)
        case "*":
            return math.prod(numbers)
        case _:
            return 0

def silver_solution(lines: list[str]) -> int:
    grid = Grid[int]([[int(number) for number in line.split()] for line in lines[:-1]])
    operations = lines[-1].split()

    return sum(perform_operation(column, operation) for column, operation in zip(grid.get_columns(0), operations))

def gold_solution(lines: list[str]) -> int:
    grid = Grid[str](lines)
    operations = lines[-1].split()

    i = 0
    current_numbers: list[int] = []
    answer = 0
    for column in grid.get_columns(" "):
        numbers = [int(number) for number in column[:-1] if number.isnumeric()]

        if numbers:
            combined_number = int("".join(map(str, numbers)))
            current_numbers.append(combined_number)
        else:
            answer += perform_operation(current_numbers, operations[i])
            i += 1
            current_numbers.clear()

    answer += perform_operation(current_numbers, operations[i])

    return answer
