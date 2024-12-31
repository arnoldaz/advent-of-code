from dataclasses import dataclass
from enum import Enum
import re

# TODO use grid
from utils.matrix import Matrix
from utils.point2d import Point2d

class Operation(Enum):
    TURN_ON = 1
    TURN_OFF = 2
    TOGGLE = 3

@dataclass
class Instruction:
    operation: Operation
    start_corner: Point2d
    end_corner: Point2d

def parse_input(lines: list[str]):
    input_regex = r"(turn on|turn off|toggle) (\d+),(\d+) through (\d+),(\d+)"
    instructions: list[Instruction] = []

    for line in lines:
        operation_string, start_x, start_y, end_x, end_y = re.findall(input_regex, line)[0]
        match operation_string:
            case "turn on":
                operation = Operation.TURN_ON
            case "turn off":
                operation = Operation.TURN_OFF
            case "toggle":
                operation = Operation.TOGGLE
            case _:
                raise ValueError("wtf")

        instructions.append(Instruction(operation, Point2d(int(start_x), int(start_y)), Point2d(int(end_x), int(end_y))))

    return instructions

# TODO: optimize
def silver_solution(lines: list[str]) -> int:
    instructions = parse_input(lines)
    grid = Matrix.create_empty(0, 1000, 1000)

    for instruction in instructions:
        for y in range(instruction.start_corner.y, instruction.end_corner.y + 1):
            for x in range(instruction.start_corner.x, instruction.end_corner.x + 1):
                point = Point2d(x, y)
                match instruction.operation:
                    case Operation.TURN_ON:
                        grid.set_symbol_2d(point, 1)
                    case Operation.TURN_OFF:
                        grid.set_symbol_2d(point, 0)
                    case Operation.TOGGLE:
                        grid.set_symbol_2d(point, 1 if grid.get_symbol_2d(point) == 0 else 0)

    return grid.count_all_character_instances(1)

# TODO: optimize
def gold_solution(lines: list[str]) -> int:
    instructions = parse_input(lines)
    grid = Matrix.create_empty(0, 1000, 1000)

    for instruction in instructions:
        for y in range(instruction.start_corner.y, instruction.end_corner.y + 1):
            for x in range(instruction.start_corner.x, instruction.end_corner.x + 1):
                point = Point2d(x, y)
                match instruction.operation:
                    case Operation.TURN_ON:
                        grid.set_symbol_2d(point, grid.get_symbol_2d(point) + 1)
                    case Operation.TURN_OFF:
                        grid.set_symbol_2d(point, max(0, grid.get_symbol_2d(point) - 1))
                    case Operation.TOGGLE:
                        grid.set_symbol_2d(point, grid.get_symbol_2d(point) + 2)

    brightness = 0

    data = grid.get_data()
    for y, line in enumerate(data):
        for x, char in enumerate(line):
            brightness += char

    return brightness
