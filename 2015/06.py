import re
from typing import Callable, NamedTuple

from utils.grid import Grid
from utils.point2d import Point2d

class Instruction(NamedTuple):
    operation: Callable[[int], int]
    start_corner: Point2d
    end_corner: Point2d

def parse_input(lines: list[str], is_gold: bool):
    input_regex = r"(turn on|turn off|toggle) (\d+),(\d+) through (\d+),(\d+)"
    instructions: list[Instruction] = []

    for line in lines:
        operation_string, start_x, start_y, end_x, end_y = re.findall(input_regex, line)[0]
        match operation_string:
            case "turn on":
                operation = (lambda x: x + 1) if is_gold else (lambda _: 1)
            case "turn off":
                operation = (lambda x: max(0, x - 1)) if is_gold else (lambda _: 0)
            case "toggle":
                operation = (lambda x: x + 2) if is_gold else (lambda x: 1 if x == 0 else 0)

        instructions.append(Instruction(operation, Point2d(int(start_x), int(start_y)), Point2d(int(end_x), int(end_y))))

    return instructions

def silver_solution(lines: list[str]) -> int:
    instructions = parse_input(lines, False)
    grid = Grid.create_empty(0, 1000, 1000)

    for instruction in instructions:
        for point, symbol in grid.iterate(instruction.start_corner, instruction.end_corner + 1):
            grid.set_symbol(point, instruction.operation(symbol))

    return grid.count_all_character_instances(1)

def gold_solution(lines: list[str]) -> int:
    instructions = parse_input(lines, True)
    grid = Grid.create_empty(0, 1000, 1000)

    for instruction in instructions:
        for point, symbol in grid.iterate(instruction.start_corner, instruction.end_corner + 1):
            grid.set_symbol(point, instruction.operation(symbol))

    return sum(sum(line) for line in grid.get_data())
