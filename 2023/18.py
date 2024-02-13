from typing import NamedTuple
from utils.point import Direction

class DigStep(NamedTuple):
    direction: Direction
    amount: int
    rgb: str

def parse_input(lines: list[str], swap_instruction: bool) -> list[DigStep]:
    dig_steps: list[DigStep] = []
    normal_direction_map = { "R": Direction.RIGHT, "D": Direction.DOWN, "L": Direction.LEFT, "U": Direction.UP }
    swapped_direction_map = { "0": Direction.RIGHT, "1": Direction.DOWN, "2": Direction.LEFT, "3": Direction.UP }

    for line in lines:
        direction_symbol, amount_string, rgb_string = line.split()
        rgb = rgb_string.removeprefix("(#").removesuffix(")")

        if not swap_instruction:
            direction = normal_direction_map.get(direction_symbol, Direction.NONE)
            amount = int(amount_string)
            dig_step = DigStep(direction, amount, rgb)
        else:
            direction = swapped_direction_map.get(rgb[-1], Direction.NONE)
            amount = int(rgb[:-1], 16)
            dig_step = DigStep(direction, amount, rgb)

        dig_steps.append(dig_step)

    return dig_steps

def calculate_area(dig_steps: list[DigStep]):
    area, perimeter = 0, 0
    current_position_x = 0

    for step in dig_steps:
        match step.direction:
            case Direction.RIGHT:
                current_position_x += step.amount
            case Direction.LEFT:
                current_position_x -= step.amount
            case Direction.UP:
                area -= current_position_x * step.amount
            case Direction.DOWN:
                area += current_position_x * step.amount
            case Direction.NONE:
                raise ValueError("Impossible to reach")

        perimeter += step.amount

    return area + (perimeter // 2) + 1

def silver_solution(lines: list[str]) -> int:
    dig_steps = parse_input(lines, False)
    return calculate_area(dig_steps)

def gold_solution(lines: list[str]) -> int:
    dig_steps = parse_input(lines, True)
    return calculate_area(dig_steps)
