# pylint: disable=unused-argument

import queue
from utils.point import INVALID_POINT, Direction, Point

class BlizzardMap:
    def __init__(self, blizzards: list[tuple[Point, Direction]], width: int, height: int):
        self.width = width
        self.height = height
        self.max_timer = 0
        self.blizzard_states: dict[int, list[tuple[Point, Direction]]] = { 0: blizzards }

    def move_blizzard(self, blizzard: tuple[Point, Direction]):
        position, direction = blizzard

        position += direction
        if position.y < 0:
            position.y = self.height - 1
        elif position.y > self.height - 1:
            position.y = 0
        elif position.x < 0:
            position.x = self.width - 1
        elif position.x > self.width - 1:
            position.x = 0

    def move_blizzards(self):
        latest_blizzard_state = self.blizzard_states[self.max_timer].copy()

        for i, blizzard in enumerate(latest_blizzard_state):
            position, direction = blizzard

            position += direction
            if position.y < 0:
                position.y = self.height - 1
            elif position.y > self.height - 1:
                position.y = 0
            elif position.x < 0:
                position.x = self.width - 1
            elif position.x > self.width - 1:
                position.x = 0

            latest_blizzard_state[i] = (position, direction)

        self.max_timer += 1
        self.blizzard_states[self.max_timer] = latest_blizzard_state

    def get_state(self, timer: int) -> list[tuple[Point, Direction]]:
        while self.max_timer < timer:
            self.move_blizzards()

        return self.blizzard_states[timer]

def parse_input(lines: list[str]) -> tuple[BlizzardMap, Point, Point]:
    blizzards: list[tuple[Point, Direction]] = []
    width = len(lines[0]) - 2
    height = len(lines) - 2

    for y, line in enumerate(lines[1:-1]):
        for x, char in enumerate(line[1:-1]):
            match char:
                case "^":
                    direction = Direction.UP
                case "<":
                    direction = Direction.LEFT
                case ">":
                    direction = Direction.RIGHT
                case "v":
                    direction = Direction.DOWN
                case ".":
                    continue
                case _:
                    raise ValueError("Unknown symbol")

            blizzards.append((Point(x, y), direction))

    blizzard_map = BlizzardMap(blizzards, width, height)
    start = Point(0, -1)
    end = Point(width - 1, height)

    return blizzard_map, start, end

def djikstra_search(blizzard_map: BlizzardMap, start: Point, end: Point) -> dict[Point, tuple[Point, int]]:
    frontier = queue.Queue[Point]()
    came_from: dict[Point, tuple[Point, int]] = {}
    cost_so_far: dict[Point, int] = {}

    frontier.put(start)
    came_from[start] = (INVALID_POINT, 0)
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()
        if current == end:
            print("wowaweeva")
            break

        for neighbor in [current + direction for direction in Direction]:
            current_cost = cost_so_far[current]
            print("getting state level", current_cost + 1)
            blizzards = blizzard_map.get_state(current_cost + 1) # cost equals to steps moved
            if any(neighbor == position for position, _ in blizzards):
                continue

            if not (0 <= neighbor.x <= blizzard_map.width - 1 and 0 <= neighbor.y <= blizzard_map.height - 1) and neighbor != end:
                continue

            new_cost = cost_so_far[current] + 1
            # if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
            if new_cost < 100:
                print(f"{new_cost=}")
                cost_so_far[neighbor] = new_cost
                came_from[neighbor] = (current, new_cost)
                frontier.put(neighbor)

    return came_from

def silver_solution(lines: list[str]) -> int:
    blizzard_map, start, end = parse_input(lines)

    result = djikstra_search(blizzard_map, start, end)

    print("end btw", end)
    for x, y in result.items():
        print(x, y)

    for key, value in blizzard_map.blizzard_states.items():
        print(f"blizzard key: {key}")
        for y in range(blizzard_map.height):
            for x in range(blizzard_map.width):
                for a, b in value:
                    if Point(x, y) == a:
                        match b:
                            case Direction.LEFT:
                                print("<", end="")
                            case Direction.RIGHT:
                                print(">", end="")
                            case Direction.UP:
                                print("^", end="")
                            case Direction.DOWN:
                                print("v", end="")
                        break
                else:
                    print(".", end="")
            print()

    return -123

def gold_solution(lines: list[str]) -> int:
    # Implement solution
    return -321
