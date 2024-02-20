import sys
from utils.point import Point

sys.setrecursionlimit(2 ** 30)

def parse_input(lines: list[str]) -> list[Point]:
    return [Point(*(int(coord) for coord in line.split(","))) for line in lines]

def calculate_surface_area(points: list[Point]) -> int:
    neighbors_map: dict[Point, int] = {}
    surface_area = 0

    for point in points:
        surface_area += 6
        if point in neighbors_map:
            surface_area -= 2 * neighbors_map[point]

        neighbors = point.get_neighbors_3d()
        for neighbor in neighbors:
            if neighbor in neighbors_map:
                neighbors_map[neighbor] += 1
            else:
                neighbors_map[neighbor] = 1

    return surface_area

def flood_fill(points: set[Point], location: Point, filled_points: set[Point]):
    if location in points or location in filled_points:
        return

    filled_points.add(location)
    for neighbor in location.get_neighbors_3d():
        flood_fill(points, neighbor, filled_points)

def get_outer_border(points: list[Point]) -> tuple[set[Point], Point, Point]:
    outer_border = set[Point]()

    min_x, max_x, min_y, max_y, min_z, max_z = sys.maxsize, 0, sys.maxsize, 0, sys.maxsize, 0
    for point in points:
        min_x = min(min_x, point.x)
        max_x = max(max_x, point.x)
        min_y = min(min_y, point.y)
        max_y = max(max_y, point.y)
        min_z = min(min_z, point.z)
        max_z = max(max_z, point.z)

    outer_min_x, outer_max_x = min_x - 2, max_x + 2
    outer_min_y, outer_max_y = min_y - 2, max_y + 2
    outer_min_z, outer_max_z = min_z - 2, max_z + 2

    for x in range(outer_min_x, outer_max_x + 1):
        for y in range(outer_min_y, outer_max_y + 1):
            for z in range(outer_min_z, outer_max_z + 1):
                if x in (outer_min_x, outer_max_x) or y in (outer_min_y, outer_max_y) or z in (outer_min_z, outer_max_z):
                    outer_border.add(Point(x, y, z))

    return outer_border, Point(outer_min_x, outer_min_y, outer_min_z), Point(outer_max_x, outer_max_y, outer_max_z)

def silver_solution(lines: list[str]) -> int:
    points = parse_input(lines)
    return calculate_surface_area(points)

def gold_solution(lines: list[str]) -> int:
    points = parse_input(lines)
    outside_border, border_min_corner, border_max_corner = get_outer_border(points)

    filled_points = set[Point]()
    flood_fill(set(points) | outside_border, border_min_corner + 1, filled_points)

    combined_area = calculate_surface_area(list(filled_points))

    border_x = (border_max_corner.x - 1) - (border_min_corner.x + 1) + 1
    border_y = (border_max_corner.y - 1) - (border_min_corner.y + 1) + 1
    border_z = (border_max_corner.z - 1) - (border_min_corner.z + 1) + 1

    outer_area = 2 * border_x * border_y + 2 * border_x * border_z + 2 * border_y * border_z

    return combined_area - outer_area
