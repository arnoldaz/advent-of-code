from utils.matrix import Matrix
from utils.point import Direction, Point

def parse_input(lines: list[str]) -> tuple[Matrix[str], Point]:
    grid = Matrix[str](lines, str)
    starting_position = grid.find_first_character_instance("S")

    return grid, starting_position

def calculate_possible_positions(starting_position: Point, grid: Matrix[str], max_iterations: int):
    current_positions: list[Point] = [starting_position]

    iterations = 0
    while iterations < max_iterations:
        iterations += 1

        new_positions = []
        for current_position in current_positions:
            for position in [current_position + direction for direction in Direction.valid_directions()]:
                if grid.in_bounds(position) and grid.get_symbol(position) != "#":
                    new_positions.append(position)

        current_positions = list(set(new_positions))

    return len(current_positions)

def silver_solution(lines: list[str]) -> int:
    grid, starting_position = parse_input(lines)
    return calculate_possible_positions(starting_position, grid, 64)

def gold_solution(_lines: list[str]) -> int:
    # Implement solution
    return -321
