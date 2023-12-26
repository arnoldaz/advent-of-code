from typing import NamedTuple
from enum import Enum

file_name = "input.txt"
with open(file_name) as file:
    lines = [line.rstrip() for line in file]

class Direction(Enum):
    No = 0
    Up = 1
    Right = 2
    Down = 3
    Left = 4

class DigStep(NamedTuple):
    direction: Direction
    amount: int
    rgb: str

dig_steps: list[DigStep] = []
width = 1
height = 1
current_width = 1
current_height = 1
min_width = 0
min_height = 0

for line in lines:
    direction_string, amount_string, rgb_string = line.split(" ")
    amount = int(amount_string)
    rgb = rgb_string.removeprefix("(#").removesuffix(")")
    match direction_string:
        case "R":
            direction = Direction.Right
            current_width += amount
        case "L":
            direction = Direction.Left
            current_width -= amount
        case "U":
            direction = Direction.Up
            current_height -= amount
        case "D":
            direction = Direction.Down
            current_height += amount
        case _:
            direction = Direction.No
    
    if current_height > height:
        height = current_height
    if current_width > width:
        width = current_width
    if current_height < min_height:
        min_height = current_height
    if current_width < min_width:
        min_width = current_width
    
    dig_steps.append(DigStep(direction, amount, rgb))

new_dig_steps: list[DigStep] = []

for step in dig_steps:
    hex_string = step.rgb[:-1]
    distance = int(hex_string, 16)
    match step.rgb[-1]:
        case "0":
            direction = Direction.Right
        case "1":
            direction = Direction.Down
        case "2":
            direction = Direction.Left
        case "3":
            direction = Direction.Up
        case _:
            direction = Direction.No
    
    new_dig_steps.append(DigStep(direction, distance, ""))

def create_2d_map(steps: list[DigStep], positive_width: int, positive_height: int, negative_width: int, negative_height: int) -> list[str]:
    map = [[["."] for _ in range(positive_width - negative_width + 1)] for _ in range(positive_height - negative_height + 1)]
    
    current_x = -negative_width + 1
    current_y = -negative_height + 1
    map[current_y][current_x][0] = "#"
    
    for step in steps:
        match step.direction:
            case Direction.Right:
                for _ in range(step.amount):
                    current_x += 1
                    map[current_y][current_x][0] = "#"
            case Direction.Left:
                for _ in range(step.amount):
                    current_x -= 1
                    map[current_y][current_x][0] = "#"
            case Direction.Up:
                for _ in range(step.amount):
                    current_y -= 1
                    map[current_y][current_x][0] = "#"
            case Direction.Down:
                for _ in range(step.amount):
                    current_y += 1
                    map[current_y][current_x][0] = "#"
    
    return ["".join("".join(single_char_list) for single_char_list in line) for line in map]

# Debugging code for visualization
# map = create_2d_map(dig_steps, width, height, min_width, min_height)
# with open("map-" + file_name, "w") as file:
#     for line in map:
#         file.write(line + "\n")

class Point:
    x: float
    y: float
    z: float

    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"{{Point: x={self.x}, y={self.y}, z={self.z}}}"

    def __repr__(self):
        return self.__str__()

def shoelace_area(vertices: list[Point]) -> float:
    n = len(vertices)
    area = 0
    for i in range(n):
        j = (i + 1) % n
        area += vertices[i].x * vertices[j].y
        area -= vertices[j].x * vertices[i].y
    area = abs(area) / 2
    return area

def invert_direction(direction: Direction) -> Direction:
    match direction:
        case Direction.Right:
            return Direction.Left
        case Direction.Left:
            return Direction.Right
        case Direction.Up:
            return Direction.Down
        case Direction.Down:
            return Direction.Up
        case Direction.No:
            return Direction.No

def get_vertices(steps: list[DigStep]) -> list[Point]:
    is_counter_clockwise = False
    first_step = steps[0]
    second_step = steps[1]

    match first_step.direction:
        case Direction.Right:
            start = Point(0.5, 0)
        case Direction.Left:
            start = Point(-0.5, 0)
        case Direction.Up:
            start = Point(0, -0.5)
        case Direction.Down:
            start = Point(0, 0.5)
        case Direction.No:
            raise Exception("No starting direction")

    vertices = [start]
    current_node = start
    previous_direction = Direction.No

    match first_step.direction, second_step.direction:
        case Direction.Right, Direction.Down:
            is_counter_clockwise = False
        case Direction.Down, Direction.Left:
            is_counter_clockwise = False
        case Direction.Left, Direction.Up:
            is_counter_clockwise = False
        case Direction.Up, Direction.Right:
            is_counter_clockwise = False
        case Direction.Right, Direction.Up:
            is_counter_clockwise = True
        case Direction.Down, Direction.Right:
            is_counter_clockwise = True
        case Direction.Left, Direction.Down:
            is_counter_clockwise = True
        case Direction.Up, Direction.Left:
            is_counter_clockwise = True
        case _:
            print(f"Weird starting directions - {first_step.direction} {second_step.direction}")


    for step in steps:
        if is_counter_clockwise:
            direction = invert_direction(step.direction)
        else:
            direction = step.direction 

        match direction:
            case Direction.Right:
                match previous_direction:
                    case Direction.Right:
                        pass
                    case Direction.Left:
                        print("Shouldn't be possible to go from LEFT to RIGHT")
                    case Direction.Up:
                        current_node = Point(current_node.x, current_node.y - 0.5)
                        vertices.append(current_node) # corner ┌+
                        current_node = Point(current_node.x + 0.5, current_node.y)
                        vertices.append(current_node)
                    case Direction.Down:
                        vertices.pop()
                        current_node = Point(current_node.x, current_node.y - 0.5)
                        vertices.append(current_node) # corner └-
                        current_node = Point(current_node.x - 0.5, current_node.y)
                        pass
                
                current_node = Point(current_node.x + step.amount, current_node.y)
                previous_direction = Direction.Right
            case Direction.Left:
                match previous_direction:
                    case Direction.Right:
                        print("Shouldn't be possible to go from RIGHT to LEFT")
                    case Direction.Left:
                        pass
                    case Direction.Up:
                        vertices.pop()
                        current_node = Point(current_node.x, current_node.y + 0.5)
                        vertices.append(current_node) # corner ┐-
                        current_node = Point(current_node.x + 0.5, current_node.y)
                    case Direction.Down:
                        current_node = Point(current_node.x, current_node.y + 0.5)
                        vertices.append(current_node) # corner ┘+
                        current_node = Point(current_node.x - 0.5, current_node.y)
                        vertices.append(current_node)

                current_node = Point(current_node.x - step.amount, current_node.y)
                previous_direction = Direction.Left
            case Direction.Up:
                match previous_direction:
                    case Direction.Right:
                        vertices.pop()
                        current_node = Point(current_node.x - 0.5, current_node.y)
                        vertices.append(current_node) # corner ┘-
                        current_node = Point(current_node.x, current_node.y + 0.5)
                    case Direction.Left:
                        current_node = Point(current_node.x - 0.5, current_node.y)
                        vertices.append(current_node) # corner └+
                        current_node = Point(current_node.x, current_node.y - 0.5)
                        vertices.append(current_node)
                    case Direction.Up:
                        pass
                    case Direction.Down:
                        print("Shouldn't be possible to go from DOWN to UP")

                current_node = Point(current_node.x, current_node.y - step.amount)
                previous_direction = Direction.Up
            case Direction.Down:
                match previous_direction:
                    case Direction.Right:
                        current_node = Point(current_node.x + 0.5, current_node.y)
                        vertices.append(current_node) # corner ┐+
                        current_node = Point(current_node.x, current_node.y + 0.5)
                        vertices.append(current_node)
                    case Direction.Left:
                        vertices.pop()
                        current_node = Point(current_node.x + 0.5, current_node.y)
                        vertices.append(current_node) # corner ┌-
                        current_node = Point(current_node.x, current_node.y - 0.5)
                    case Direction.Up:
                        print("Shouldn't be possible to go from UP to DOWN")
                    case Direction.Down:
                        pass
                
                current_node = Point(current_node.x, current_node.y + step.amount)
                previous_direction = Direction.Down

        vertices.append(current_node)

    # Add additional leftover piece for the last movement
    match previous_direction:
        case Direction.Right:
            vertices.append(Point(current_node.x + 0.5, current_node.y))
        case Direction.Left:
            vertices.append(Point(current_node.x - 0.5, current_node.y))
        case Direction.Up:
            vertices.append(Point(current_node.x, current_node.y - 0.5))
        case Direction.Down:
            vertices.append(Point(current_node.x, current_node.y + 0.5))

    return vertices

print(f"{int(shoelace_area(get_vertices(dig_steps)))=}")
print(f"{int(shoelace_area(get_vertices(new_dig_steps)))=}")
