from typing import Iterator, NamedTuple
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

def get_outside_sensor_path(sensor: Sensor) -> Iterator[Point]:
    distance = manhattan_distance(sensor.location, sensor.closest_beacon)
    left = Point(sensor.location.x - distance - 1, sensor.location.y)
    right = Point(sensor.location.x + distance + 1, sensor.location.y)
    up = Point(sensor.location.x, sensor.location.y - distance - 1)
    down = Point(sensor.location.x, sensor.location.y + distance + 1)

    left_up, up_right, right_down, down_left = Point(1, -1), Point(1, 1), Point(-1, 1), Point(-1, -1)
    current_left, current_up, current_right, current_down = left, up, right, down

    while current_left != up:
        current_left += left_up
        current_up += up_right
        current_right += right_down
        current_down += down_left
        yield current_left
        yield current_up
        yield current_right
        yield current_down

def gold_solution(lines: list[str]) -> int:
    sensors = parse_input(lines)
    building_locations = set(sensor.closest_beacon for sensor in sensors) | set(sensor.location for sensor in sensors)
    distances = [manhattan_distance(sensor.location, sensor.closest_beacon) for sensor in sensors]

    for sensor in sensors:
        for point in get_outside_sensor_path(sensor):
            if point in building_locations:
                continue

            blocked = any(manhattan_distance(point, sensor.location) <= distances[i] for i, sensor in enumerate(sensors))
            if not blocked and 0 <= point.x <= 4_000_000 and 0 <= point.y <= 4_000_000:
                return point.x * 4_000_000 + point.y

    return -1
