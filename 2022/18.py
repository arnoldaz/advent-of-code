# pylint: disable=unused-argument

import sys
from utils.point import INVALID_POINT, Point

sys.setrecursionlimit(2 ** 30)

def parse_input(lines: list[str]) -> list[Point]:
    return [Point(*(int(coord) for coord in line.split(","))) for line in lines]

def silver_solution(lines: list[str]) -> int:
    points = parse_input(lines)

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

def flood_fill_3d(points: list[Point], location: Point, filled_points: list[Point]):
    if location in points or location in filled_points:
        return

    print(location)

    filled_points.append(location)
    for neighbor in location.get_neighbors_3d():
        flood_fill_3d(points, neighbor, filled_points)

def is_inside_point(point_to_check: Point, points: list[Point]) -> bool:
    x_less = any(point.x < point_to_check.x and point.y == point_to_check.y and point.z == point_to_check.z for point in points)
    x_more = any(point.x > point_to_check.x and point.y == point_to_check.y and point.z == point_to_check.z for point in points)

    y_less = any(point.y < point_to_check.y and point.x == point_to_check.x and point.z == point_to_check.z for point in points)
    y_more = any(point.y > point_to_check.y and point.x == point_to_check.x and point.z == point_to_check.z for point in points)

    z_less = any(point.z < point_to_check.z and point.y == point_to_check.y and point.x == point_to_check.x for point in points)
    z_more = any(point.z > point_to_check.z and point.y == point_to_check.y and point.x == point_to_check.x for point in points)

    return x_less and x_more and y_less and y_more and z_less and z_more

def get_flood_fill_length(points: list[Point], location: Point):
    filled_points: list[Point] = []
    flood_fill_3d(points, location, filled_points)


    return len(filled_points)

def gold_solution(lines: list[str]) -> int:
    points = parse_input(lines)

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

    inside_points = []

    for neighbor in neighbors_map:
        if neighbor not in points and is_inside_point(neighbor, points):
            inside_points.append(neighbor)

    print(len(inside_points))

    for inside in inside_points:
        print(get_flood_fill_length(points, inside))

    return -1

    inside_point = INVALID_POINT

    for key, value in neighbors_map.items():
        if value == 6 and key not in points:
            inside_point = key
            break

    print(inside_point)

    filled_points: list[Point] = []
    flood_fill_3d(points, inside_point, filled_points)

    print(filled_points)

    new_neighbors_map: dict[Point, int] = {}
    new_surface_area = 0

    for point in filled_points:
        new_surface_area += 6
        if point in new_neighbors_map:
            new_surface_area -= 2 * new_neighbors_map[point]

        neighbors = point.get_neighbors_3d()
        for neighbor in neighbors:
            if neighbor in new_neighbors_map:
                new_neighbors_map[neighbor] += 1
            else:
                new_neighbors_map[neighbor] = 1

    print(new_surface_area)

    # found_something = True

    # while found_something:
    #     found_something = False
    #     new_keys = []
    #     parsed_key = INVALID_POINT

    #     for key, value in neighbors_map.items():
    #         if value == 6 and key not in points:
    #             found_something = True
    #             surface_area -= 6

    #             new_keys = key.get_neighbors_3d()
    #             parsed_key = key

    #     if found_something:
    #         for neighbor in new_keys:
    #             if neighbor in neighbors_map:
    #                 neighbors_map[neighbor] += 1
    #             else:
    #                 neighbors_map[neighbor] = 1

    #         del neighbors_map[parsed_key]

    return surface_area - new_surface_area
