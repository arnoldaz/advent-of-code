from enum import Enum
from typing import NamedTuple, Optional
import uuid
import sys
import math

# sys.setrecursionlimit(2 ** 30)

with open("input.txt") as file:
    lines = [line.rstrip() for line in file]

class Point:
    x: int
    y: int
    z: int

    def __init__(self, x: int = 0, y: int = 0, z: int = 0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"{{Point: x={self.x}, y={self.y}, z={self.z}}}"

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __add__(self, other):
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y, self.z + other.z)
        
        if isinstance(other, int):
            return Point(self.x + other, self.y + other, self.z + other)
        
        raise Exception(f"Unrecognized variable added to Point - {other}")

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y and self.z == other.z
        
        raise Exception(f"Unrecognized variable compared to Point - {other}")

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
    except Exception:
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

    for i in range(len(hailstones)):
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

_hailstones = get_initial_data(lines, True)
print(f"{count_intersections_in_area(_hailstones, 200000000000000, 400000000000000)=}")
