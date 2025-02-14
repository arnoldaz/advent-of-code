from utils.grid import Grid
from utils.point2d import Direction2d

def parse_input(lines: list[str]) -> list[list[Direction2d]]:
    return [[Direction2d.from_character(char) for char in line] for line in lines]

def calculate_numpad_code(numpad: Grid[str], start_button: str, instructions: list[list[Direction2d]]) -> str:
    code: list[str] = []
    current_position = numpad.find_first_character_instance(start_button)

    for instruction in instructions:
        for move in instruction:
            next_position = current_position + move
            if numpad.in_bounds(next_position) and numpad.get_symbol(next_position):
                current_position += move

        code.append(numpad.get_symbol(current_position))

    return "".join(code)

def silver_solution(lines: list[str]) -> str:
    instructions = parse_input(lines)
    numpad = Grid[str]([
        ["1", "2", "3"],
        ["4", "5", "6"],
        ["7", "8", "9"],
    ])

    return calculate_numpad_code(numpad, "5", instructions)

def gold_solution(lines: list[str]) -> str:
    instructions = parse_input(lines)
    numpad = Grid[str]([
        ["",  "",  "1", "",  ""],
        ["",  "2", "3", "4", ""],
        ["5", "6", "7", "8", "9"],
        ["",  "A", "B", "C", ""],
        ["",  "",  "D", "",  ""],
    ])

    return calculate_numpad_code(numpad, "5", instructions)
