from functools import cache

from utils.grid import Grid
from utils.point2d import Point2d

def get_keypads() -> tuple[Grid[str], Grid[str]]:
    number_keypad = Grid[str]([
        ["7", "8", "9"],
        ["4", "5", "6"],
        ["1", "2", "3"],
        [ "", "0", "A"],
    ])
    direction_keypad = Grid[str]([
        [ "", "^", "A"],
        ["<", "v", ">"],
    ])

    return number_keypad, direction_keypad

def generate_path_map(keypad: Grid[str]) -> dict[tuple[str, str], str]:
    path_map: dict[tuple[str, str], str] = {}
    for p1, num1 in keypad.iterate():
        for p2, num2 in keypad.iterate():
            if not num1 or not num2:
                continue

            # Order: left -> down -> up -> right
            path  = "<" * (p1.x - p2.x)
            path += "v" * (p2.y - p1.y)
            path += "^" * (p1.y - p2.y)
            path += ">" * (p2.x - p1.x)

            # Reverse the path if going through empty point
            if not keypad.get_symbol(Point2d(p1.x, p2.y)) or not keypad.get_symbol(Point2d(p2.x, p1.y)):
                path = path[::-1]

            path_map[(num1, num2)] = path + "A"

    return path_map

def get_path_length(initial_code: str, iterations: int, number_path_map: dict[tuple[str, str], str], direction_path_map: dict[tuple[str, str], str]) -> int:
    @cache
    def get_path_length_recursive(code: str, depth: int) -> int:
        if depth == iterations:
            return len(code)

        current_symbol = "A"
        total_length = 0
        for move in code:
            next_iteration_code = (
                number_path_map[(current_symbol, move)]
                if depth == 0
                else direction_path_map[(current_symbol, move)]
            )
            total_length += get_path_length_recursive(next_iteration_code, depth + 1)
            current_symbol = move

        return total_length

    return get_path_length_recursive(initial_code, 0)

def silver_solution(lines: list[str]) -> int:
    number_keypad, direction_keypad = get_keypads()
    number_path_map = generate_path_map(number_keypad)
    direction_path_map = generate_path_map(direction_keypad)

    return sum(
        int(code[:-1]) * get_path_length(code, 3, number_path_map, direction_path_map)
        for code in lines
    )

def gold_solution(lines: list[str]) -> int:
    number_keypad, direction_keypad = get_keypads()
    number_path_map = generate_path_map(number_keypad)
    direction_path_map = generate_path_map(direction_keypad)

    return sum(
        int(code[:-1]) * get_path_length(code, 26, number_path_map, direction_path_map)
        for code in lines
    )
