from dataclasses import dataclass

from utils.point2d import Direction2d, Point2d
from utils.string import get_ints

@dataclass
class Robot:
    position: Point2d
    velocity: Point2d

def parse_input(lines: list[str]) -> list[Robot]:
    return [
        Robot(Point2d(position_x, position_y), Point2d(velocity_x, velocity_y))
        for line in lines
        for position_x, position_y, velocity_x, velocity_y in [get_ints(line, True)]
    ]

def move_robots(robots: list[Robot], width: int, height: int, time: int):
    for _ in range(time):
        for robot in robots:
            new_position = robot.position + robot.velocity
            x, y = new_position.x, new_position.y

            if x < 0:
                x += width
            elif x >= width:
                x -= width

            if y < 0:
                y += height
            elif y >= height:
                y -= height

            robot.position = Point2d(x, y)

def find_easter_egg(robots: list[Robot]) -> bool:
    robot_positions = set(robot.position for robot in robots)
    for robot in robots:
        for i in range(1, 10):
            if (robot.position + Direction2d.RIGHT * i) not in robot_positions:
                break
        else:
            return True

    return False

def calculate_safety_factor(robots: list[Robot], width: int, height: int) -> int:
    half_width = width // 2
    half_height = height // 2

    q1_sum, q2_sum, q3_sum, q4_sum = 0, 0, 0, 0

    for robot in robots:
        if robot.position.x < half_width and robot.position.y < half_height:
            q1_sum += 1
        elif robot.position.x > half_width and robot.position.y < half_height:
            q2_sum += 1
        elif robot.position.x < half_width and robot.position.y > half_height:
            q3_sum += 1
        elif robot.position.x > half_width and robot.position.y > half_height:
            q4_sum += 1

    return q1_sum * q2_sum * q3_sum * q4_sum

def silver_solution(lines: list[str]) -> int:
    robots = parse_input(lines)
    width, height = 101, 103
    time = 100

    move_robots(robots, width, height, time)

    return calculate_safety_factor(robots, width, height)

def gold_solution(lines: list[str]) -> int:
    robots = parse_input(lines)
    width, height = 101, 103

    for i in range(10_000):
        move_robots(robots, width, height, 1)
        if find_easter_egg(robots):
            return i + 1

    return -1
