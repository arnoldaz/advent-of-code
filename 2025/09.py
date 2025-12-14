import sys
from itertools import combinations
from utils.grid import Grid
from utils.point2d import Point2d

sys.setrecursionlimit(2 ** 30)

def parse_input(lines: list[str]) -> list[Point2d]:
    return [Point2d(*map(int, line.split(","))) for line in lines]

def silver_solution(lines: list[str]) -> int:
    points = parse_input(lines)

    return max(
        (abs(p1.x - p2.x) + 1) * (abs(p1.y - p2.y) + 1)
        for p1, p2
        in combinations(points, 2)
    )

def gold_solution(lines: list[str]) -> int:
    points = parse_input(lines)

    # Extract unique x and y values
    xs = sorted(set(point.x for point in points))
    ys = sorted(set(point.y for point in points))

    # Create compression map (value -> index)
    x_map = {v: i for i, v in enumerate(xs)}
    y_map = {v: i for i, v in enumerate(ys)}

    # Create compressed coordinates representing indexes between the values instead of the values themselves
    compressed = [Point2d(x_map[point.x], y_map[point.y]) for point in points]

    grid = Grid.create_empty(".", max(point.x + 1 for point in compressed), max(point.y + 1 for point in compressed))

    # Draw polygon lines on the grid from the compressed points
    for point1, point2 in zip(compressed, compressed[1:] + compressed[:1]):
        # Vertical edges
        if point1.x == point2.x: 
            for y in range(min(point1.y, point2.y), max(point1.y, point2.y)):
                grid.set_symbol(Point2d(point1.x, y), "#")

        # Horizontal edges
        if point1.y == point2.y: 
            for x in range(min(point1.x, point2.x), max(point1.x, point2.x)):
                grid.set_symbol(Point2d(x, point1.y), "#")

    # Assuming the input is clean and doesn't have peninsulas made only from walls, there should be an empty space on bot right of the first corner
    inside_point = grid.find_first_character_instance("#") + Point2d(1, 1)

    def flood_fill(location: Point2d):
        if grid.get_symbol(location) == "#":
            return

        grid.set_symbol(location, "#")
        for neighbor in grid.get_neighbors(location):
            flood_fill(neighbor)

    flood_fill(inside_point)

    largest_area = 0
    for i, point1 in enumerate(points):
        compressed_point1 = Point2d(x_map[point1.x], y_map[point1.y])
        for point2 in points[i+1:]:
            compressed_point2 = Point2d(x_map[point2.x], y_map[point2.y])

            width = abs(point1.x - point2.x) + 1
            height = abs(point1.y - point2.y) + 1
            area = width * height

            if area <= largest_area:
                continue

            min_x = min(compressed_point1.x, compressed_point2.x)
            max_x = max(compressed_point1.x, compressed_point2.x)
            min_y = min(compressed_point1.y, compressed_point2.y)
            max_y = max(compressed_point1.y, compressed_point2.y)

            vertical_sides_inside = all(
                grid.get_symbol(Point2d(x, y)) == "#"
                for y in range(min_y, max_y + 1)
                for x in (min_x, max_x)
            )

            if not vertical_sides_inside:
                continue

            horizontal_sides_inside = all(
                grid.get_symbol(Point2d(x, y)) == "#"
                for x in range(min_x, max_x + 1)
                for y in (min_y, max_y)
            )

            if not horizontal_sides_inside:
                continue

            largest_area = area

    return largest_area
