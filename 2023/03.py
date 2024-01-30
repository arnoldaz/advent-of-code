import re
from typing import Callable
from utils.point import Point

def is_non_empty_symbol(char: str) -> bool:
    return char != "." and not char.isdigit()

def is_gear_symbol(char: str) -> bool:
    return char == "*"

def is_valid_symbol_adjacent(matrix: list[str], start_position: int, end_position: int, line_number: int, valid_symbol_function: Callable[[str], bool]) -> tuple[bool, Point]:
    # top line
    if line_number != 0:
        upper_line = matrix[line_number - 1]
        for i in range(max(start_position, 0), min(end_position + 1, len(upper_line))):
            if valid_symbol_function(upper_line[i]):
                return True, Point(line_number - 1, i)

    # bot line
    if line_number != len(matrix) - 1:
        lower_line = matrix[line_number + 1]
        for i in range(max(start_position, 0), min(end_position + 1, len(lower_line))):
            if valid_symbol_function(lower_line[i]):
                return True, Point(line_number + 1, i)

    current_line = matrix[line_number]

    # left side
    if start_position >= 0 and valid_symbol_function(current_line[start_position]):
        return True, Point(line_number, start_position)

    # right side
    if end_position <= len(current_line) - 1 and valid_symbol_function(current_line[end_position]):
        return True, Point(line_number, end_position)

    return False, Point(-1, -1)

def silver_solution(lines: list[str]) -> int:
    final_sum = 0
    for y, line in enumerate(lines):
        numbers_data = [(int(number.group(0)), number.start(0) - 1, number.end(0)) for number in re.finditer(r"\b\d+\b", line)]
        final_sum += sum(number for number, start_position, end_position in numbers_data if is_valid_symbol_adjacent(lines, start_position, end_position, y, is_non_empty_symbol)[0])

    return final_sum

def gold_solution(lines: list[str]) -> int:
    gear_map: dict[Point, list[int]] = {}
    for y, line in enumerate(lines):
        numbers_data = [(int(number.group(0)), number.start(0) - 1, number.end(0)) for number in re.finditer(r"\b\d+\b", line)]
        for number, start_position, end_position in numbers_data:
            is_number_valid, gear_position = is_valid_symbol_adjacent(lines, start_position, end_position, y, is_gear_symbol)
            if is_number_valid:
                gear_map.setdefault(gear_position, []).append(number)

    return sum(values[0] * values[1] for values in gear_map.values() if len(values) == 2)
