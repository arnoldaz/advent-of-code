import math
from itertools import combinations
from utils.point3d import Point3d

def parse_input(lines: list[str]) -> list[Point3d]:
    return [Point3d(*map(int, line.split(","))) for line in lines]

def get_distance_map(points: list[Point3d]) -> dict[float, tuple[Point3d, Point3d]]:
    distance_map: dict[float, tuple[Point3d, Point3d]] = {}
    for point1, point2 in combinations(points, 2):
        distance_squared = point1.euclidean_distance_squared(point2)
        distance_map[distance_squared] = (point1, point2)

    return distance_map

def get_updated_circuits(circuits: list[set[Point3d]], point1: Point3d, point2: Point3d) -> list[set[Point3d]]:
    valid_circuits = [c for c in circuits if point1 in c or point2 in c]

    if not valid_circuits:
        return circuits + [{point1, point2}]

    merged_set = {point1, point2}.union(*valid_circuits)
    updated_circuits = [c for c in circuits if c not in valid_circuits]
    updated_circuits.append(merged_set)

    return updated_circuits

def silver_solution(lines: list[str]) -> int:
    points = parse_input(lines)
    distance_map = get_distance_map(points)
    sorted_distances = sorted(distance_map.keys())

    circuits: list[set[Point3d]] = []
    for distance in sorted_distances[:1000]:
        point1, point2 = distance_map[distance]
        circuits = get_updated_circuits(circuits, point1, point2)

    return math.prod(sorted((len(c) for c in circuits), reverse=True)[:3])

def gold_solution(lines: list[str]) -> int:
    points = parse_input(lines)
    distance_map = get_distance_map(points)
    sorted_distances = sorted(distance_map.keys())

    circuits: list[set[Point3d]] = []
    for distance in sorted_distances:
        point1, point2 = distance_map[distance]
        circuits = get_updated_circuits(circuits, point1, point2)

        if len(circuits) == 1 and len(circuits[0]) == len(points):
            return point1.x * point2.x

    return -1
