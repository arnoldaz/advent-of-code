from decimal import DivisionByZero
from typing import NamedTuple
import math
from utils.point import Point

class Hailstone(NamedTuple):
    position: Point
    velocity: Point

def get_initial_data(lines: list[str], ignore_z_axis: bool) -> list[Hailstone]:
    hailstones: list[Hailstone] = []

    for line in lines:
        position_str, velocity_str = line.split(" @ ")
        position_x, position_y, position_z = [int(x) for x in position_str.split(", ")]
        velocity_x, velocity_y, velocity_z = [int(x) for x in velocity_str.split(", ")]

        if ignore_z_axis:
            hailstones.append(Hailstone(Point(position_x, position_y), Point(velocity_x, velocity_y)))
        else:
            hailstones.append(Hailstone(Point(position_x, position_y, position_z), Point(velocity_x, velocity_y, velocity_z)))

    return hailstones

def generate_2d_intersection(hailstone1: Hailstone, hailstone2: Hailstone) -> tuple[float, float]:
    # https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection
    x1, x2 = hailstone1.position.x, hailstone1.position.x + hailstone1.velocity.x
    y1, y2 = hailstone1.position.y, hailstone1.position.y + hailstone1.velocity.y

    x3, x4 = hailstone2.position.x, hailstone2.position.x + hailstone2.velocity.x
    y3, y4 = hailstone2.position.y, hailstone2.position.y + hailstone2.velocity.y

    try:
        px = ( (x1*y2-y1*x2)*(x3-x4)-(x1-x2)*(x3*y4-y3*x4) ) / ( (x1-x2)*(y3-y4)-(y1-y2)*(x3-x4) )
        py = ( (x1*y2-y1*x2)*(y3-y4)-(y1-y2)*(x3*y4-y3*x4) ) / ( (x1-x2)*(y3-y4)-(y1-y2)*(x3-x4) )
    except ZeroDivisionError:
        return (math.inf, math.inf)

    return (px, py)

def dot_product(vector1: tuple[float, float], vector2: tuple[float, float]) -> float:
    return sum(x * y for x, y in zip(vector1, vector2))

def is_point_in_direction(start_point: tuple[float, float], direction_vector: tuple[float, float], test_point: tuple[float, float], threshold: float = 0.99) -> bool:
    start_test_vector = tuple[float, float](test - start for start, test in zip(start_point, test_point))

    dot_product_value = dot_product(direction_vector, start_test_vector)

    return dot_product_value > threshold

def count_intersections_in_area(hailstones: list[Hailstone], test_area_min: int, test_area_max: int) -> int:
    intersections = 0

    for i in range(len(hailstones)): # pylint: disable=consider-using-enumerate
        for j in range(i + 1, len(hailstones)):
            point = generate_2d_intersection(hailstones[i], hailstones[j])
            if point[0] == math.inf or point[1] == math.inf:
                # print("inf")
                continue

            if test_area_min <= point[0] <= test_area_max and test_area_min <= point[1] <= test_area_max:
                if not is_point_in_direction((hailstones[i].position.x, hailstones[i].position.y), (hailstones[i].velocity.x, hailstones[i].velocity.y), point):
                    # print("behind first")
                    continue

                if not is_point_in_direction((hailstones[j].position.x, hailstones[j].position.y), (hailstones[j].velocity.x, hailstones[j].velocity.y), point):
                    # print("behind second")
                    continue

                # print(f"adding intersection {point}")
                intersections += 1
            # else:
            #     print(f"not adding {point}")

    return intersections

def silver_solution(lines: list[str]) -> int:
    _hailstones = get_initial_data(lines, True)
    return count_intersections_in_area(_hailstones, 200000000000000, 400000000000000)

def gold_solution(_lines: list[str]) -> int:
    # Implement solution
    return -321
