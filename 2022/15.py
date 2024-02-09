from typing import NamedTuple
from utils.point import Point
from utils.string import get_ints

class Sensor(NamedTuple):
    location: Point
    closest_beacon: Point

def parse_input(lines: list[str]) -> list[Sensor]:
    sensors: list[Sensor] = []
    for line in lines:
        sensor_x, sensor_y, beacon_x, beacon_y = get_ints(line, True)
        sensors.append(Sensor(Point(sensor_x, sensor_y), Point(beacon_x, beacon_y)))
    return sensors

def manhattan_distance(point1: Point, point2: Point) -> int:
    return abs(point1.x - point2.x) + abs(point1.y - point2.y)

def silver_solution(lines: list[str]) -> int:
    sensors = parse_input(lines)
    y = 2_000_000

    distances = [manhattan_distance(sensor.location, sensor.closest_beacon) for sensor in sensors]
    max_distance = max(distances)

    min_x = min(sensor.closest_beacon.x for sensor in sensors) - max_distance
    max_x = max(sensor.closest_beacon.x for sensor in sensors) + max_distance

    counter = 0
    for x in range(min_x, max_x + 1):
        point = Point(x, y)
        block = False
        for i, sensor in enumerate(sensors):
            if point != sensor.closest_beacon and manhattan_distance(point, sensor.location) <= distances[i]:
                block = True
                break

        if block:
            counter += 1

    return counter

def gold_solution(lines: list[str]) -> int:
    return -1
