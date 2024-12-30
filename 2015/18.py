from collections import Counter
from utils.grid import Grid
from utils.point2d import Point2d

def parse_input(lines: list[str]) -> tuple[set[Point2d], int, int]:
    live_cells = {point for point, symbol in Grid.iterate_lines(lines) if symbol == "#"}
    return live_cells, len(lines[0]), len(lines)

def silver_solution(lines: list[str]) -> int:
    live_cells, width, height = parse_input(lines)

    for _ in range(100):
        expanded_cells = list(live_cells)
        for cell in live_cells:
            expanded_cells += cell.get_neighbors(width, height, True)

        live_cells = set(
            point
            for point, counter in Counter(expanded_cells).items()
            if counter == 3 or (counter == 4 and point in live_cells)
        )

    return len(live_cells)

def gold_solution(lines: list[str]) -> int:
    live_cells, width, height = parse_input(lines)
    corners = set([Point2d(0, 0), Point2d(width - 1, 0), Point2d(0, height - 1), Point2d(width - 1, height - 1)])
    live_cells.update(corners)

    for _ in range(100):
        expanded_cells = list(live_cells)
        for cell in live_cells:
            expanded_cells += cell.get_neighbors(width, height, True)

        live_cells = set(
            point
            for point, counter in Counter(expanded_cells).items()
            if counter == 3 or (counter == 4 and point in live_cells)
        ).union(corners)

    return len(live_cells)
