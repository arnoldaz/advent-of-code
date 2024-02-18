from utils.matrix import Matrix
from utils.point import Direction, Point

def parse_input(lines: list[str], create_5x5: bool) -> tuple[Matrix[str], Point]:
    new_lines: list[str] = []

    if create_5x5:
        for i in range(5):
            for line in lines:
                if i == 2:
                    new_line = line.replace("S", ".")
                    new_lines.append(new_line * 2 + line + new_line * 2)
                else:
                    new_line = line.replace("S", ".")
                    new_lines.append(new_line * 5)
    else:
        new_lines = lines

    grid = Matrix[str](new_lines, str)
    starting_position = grid.find_first_character_instance("S")

    return grid, starting_position

def calculate_possible_positions(starting_position: Point, grid: Matrix[str], iteration_thresholds: list[int]) -> list[int]:
    current_positions: list[Point] = [starting_position]
    directions = Direction.valid_directions()

    lengths_at_thresholds: list[int] = []
    threshold_index = 0

    iteration = 0
    while iteration < iteration_thresholds[threshold_index]:
        iteration += 1

        new_positions = set[Point]()
        for current_position in current_positions:
            for position in [current_position + direction for direction in directions]:
                if grid.get_symbol(position) != "#":
                    new_positions.add(position)

        current_positions = list(new_positions)

        if iteration in iteration_thresholds:
            lengths_at_thresholds.append(len(current_positions))
            threshold_index = min(threshold_index + 1, len(iteration_thresholds) - 1)

    return lengths_at_thresholds

def silver_solution(lines: list[str]) -> int:
    grid, starting_position = parse_input(lines, False)
    return calculate_possible_positions(starting_position, grid, [64])[0]

def gold_solution(lines: list[str]) -> int:
    grid, starting_position = parse_input(lines, True)

    x0, x1, x2 = 65, 65 + 131, 65 + 2 * 131
    y0, y1, y2, *_ = calculate_possible_positions(starting_position, grid, [x0, x1, x2])

    y01 = (y1 - y0) / (x1 - x0)
    y12 = (y2 - y1) / (x2 - x1)
    y012 = (y12 - y01) / (x2 - x0)

    n = 26501365
    return int(y0 + y01 * (n - x0) + y012 * (n - x0) * (n - x1))
