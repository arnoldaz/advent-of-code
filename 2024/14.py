import re
from typing import NamedTuple
from utils.point import Point

# TODO

class Robot(NamedTuple):
    position: Point
    velocity: Point

def parse_input(lines: list[str]) -> list[Robot]:
    robot_regex = r"p=(\d+),(\d+) v=(-*\d+),(-*\d+)"
    robots: list[Robot] = []

    for line in lines:
        robot_match = re.match(robot_regex, line)
        if not robot_match:
            raise ValueError("Wrong input")

        robot = Robot(
            Point(int(robot_match.group(1)), int(robot_match.group(2))),
            Point(int(robot_match.group(3)), int(robot_match.group(4)))
        )
        robots.append(robot)

    return robots

def write_to_file(robots: list[Robot], width: int, height: int, second: int):
    with open("temp/robots2.txt", "a", encoding="utf-8") as file:
        file.write(f"============================= SECOND {second} =============================\n")
        for y in range(height):
            for x in range(width):
                a = sum(1 for robot in robots if robot.position == Point(x, y))
                if a == 0:
                    file.write(".")
                else:
                    file.write(str(a))
            file.write("\n")

def silver_solution(lines: list[str]) -> int:
    robots = parse_input(lines)

    # width = 11
    # height = 7
    width = 101
    height = 103
    end_seconds = 100

    for s in range(end_seconds):
        for i, robot in enumerate(robots):
            pos = robot.position + robot.velocity
            x, y = pos.x, pos.y
            if pos.x < 0:
                x += width
            elif pos.x >= width:
                x -= width
            
            if pos.y < 0:
                y += height
            elif pos.y >= height:
                y -= height

            pos = Point(x, y)
            robots[i] = Robot(pos, robot.velocity)

    half_width = width // 2
    half_height = height // 2

    q1_sum, q2_sum, q3_sum, q4_sum = 0, 0, 0, 0

    for robot in robots:
        if robot.position.x < half_width and robot.position.y < half_height:
            q1_sum += 1
        if robot.position.x > half_width and robot.position.y < half_height:
            q2_sum += 1
        if robot.position.x < half_width and robot.position.y > half_height:
            q3_sum += 1
        if robot.position.x > half_width and robot.position.y > half_height:
            q4_sum += 1

    return q1_sum * q2_sum * q3_sum * q4_sum

def gold_solution(lines: list[str]) -> int:
    # robots = parse_input(lines)

    # width = 101
    # height = 103
    # end_seconds = 10000

    # for s in range(end_seconds):
    #     for i, robot in enumerate(robots):
    #         pos = robot.position + robot.velocity
    #         x, y = pos.x, pos.y
    #         if pos.x < 0:
    #             x += width
    #         elif pos.x >= width:
    #             x -= width
            
    #         if pos.y < 0:
    #             y += height
    #         elif pos.y >= height:
    #             y -= height

    #         pos = Point(x, y)
    #         robots[i] = Robot(pos, robot.velocity)

    #     write_to_file(robots, width, height, s)
    #     print(s)

    # Visually found using the text file at second 6511 (counting from 0) using the code above
    return 6512
