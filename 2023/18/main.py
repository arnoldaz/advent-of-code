import sys
from typing import NamedTuple
from enum import Enum

file_name = "input-test.txt"
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

# print(f"{width=} {height=} {min_width=} {min_height=}")

map = create_2d_map(dig_steps, width, height, min_width, min_height)
with open("map-" + file_name, "w") as file:
    for line in map:
        file.write(line + "\n")

def flood_fill(matrix, row, col, fill_char, boundary_char):
    if row < 0 or row >= len(matrix) or col < 0 or col >= len(matrix[0]) or matrix[row][col] != ".":
        return

    matrix[row][col] = fill_char

    flood_fill(matrix, row + 1, col, fill_char, boundary_char)  # Down
    flood_fill(matrix, row - 1, col, fill_char, boundary_char)  # Up
    flood_fill(matrix, row, col + 1, fill_char, boundary_char)  # Right
    flood_fill(matrix, row, col - 1, fill_char, boundary_char)  # Left

def find_cells_inside_polygon(matrix, inside_row, inside_col):
    fill_char = "#" 
    boundary_char = "#"

    flood_fill(matrix, inside_row, inside_col, fill_char, boundary_char)

def check_inside(x: int, y: int, map: list[str]) -> bool:
    line = map[y]
    
    horizontal_walls: list[int] = []
    for i, char in enumerate(line):
        if char == "#" and (i == 0 or line[i-1] != "#"):
            horizontal_walls.append(i)

    left_counter = 0
    for wall in horizontal_walls:
        if wall < x:
            left_counter += 1
    
    return left_counter % 2 == 1
    
    # line = map[y]
    
    # horizontal_wall_left = sys.maxsize
    # horizontal_wall_right = -1
    # for i, char in enumerate(line):
    #     if char == "#":
    #         if i < horizontal_wall_left:
    #             horizontal_wall_left = i
    #         if i > horizontal_wall_right:
    #             horizontal_wall_right = i
    
    # if not horizontal_wall_left < x < horizontal_wall_right:
    #     return False
    
    # column = ["".join(line[x]) for line in map]
    # vertical_wall_up = sys.maxsize
    # vertical_wall_down = -1
    # for i, char in enumerate(column):
    #     if char == "#":
    #         if i < vertical_wall_up:
    #             vertical_wall_up = i
    #         if i > vertical_wall_down:
    #             vertical_wall_down = i
    
    # if not vertical_wall_up < y < vertical_wall_down:
    #     return False
    
    return True

# filled_map = [[["."] for _ in range(width - min_width + 1)] for _ in range(height - min_height + 1)]
# filled_count = 0
# for y, line in enumerate(map):
#     for x, char in enumerate(line):
#         if char == "#" or check_inside(x, y, map):
#             filled_count += 1
#             filled_map[y][x][0] = "#"

inside_row = -1
inside_col = -1

for y, line in enumerate(map):
    for x, char in enumerate(line):
        if char == "." and check_inside(x, y, map):
            inside_row = y
            inside_col = x
            break
    if inside_col != -1:
        break

print(f"{inside_row=} {inside_col=}")

sys.setrecursionlimit(1_000_000)

matrix = [list(row) for row in map]
find_cells_inside_polygon(matrix, 50, 300)



filled_map = ["".join("".join(single_char_list) for single_char_list in line) for line in matrix]
with open("map-filled-" + file_name, "w") as file:
    for line in filled_map:
        file.write(line + "\n")

filled_count = 0
for line in filled_map:
    for char in line:
        if char == "#":
            filled_count += 1

print(f"{filled_count=}")

#####################################################################

test_vertices = [(0, 0), (10, 0), (10, -20), (0, -20)]

test_vertices = [(-1, 0), (-1, -1), (-1, -0.99), (-2, -1), (-2, 1), (-1, 0.99), (-1, 1)]

def shoelace_area(vertices):
    n = len(vertices)
    area = 0
    for i in range(n):
        j = (i + 1) % n
        area += vertices[i][0] * vertices[j][1]
        area -= vertices[j][0] * vertices[i][1]
    area = abs(area) / 2
    return area

area = shoelace_area(test_vertices)
print(f"{area=}")

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

# start = (0, 0)
# vertices = [start]
# current_node = start

# for step in new_dig_steps:
#     match step.direction:
#         case Direction.Right:
#             current_node = (current_node[0] + step.amount, current_node[1])
#         case Direction.Left:
#             current_node = (current_node[0] - step.amount, current_node[1])
#         case Direction.Up:
#             current_node = (current_node[0], current_node[1] - step.amount)
#         case Direction.Down:
#             current_node = (current_node[0], current_node[1] + step.amount)

#     vertices.append(current_node)

# print(vertices)
# new_area = shoelace_area(vertices)
# print(f"{new_area=}")

###

start = (0, 0)
vertices = [start]
current_node = start


for step in dig_steps:
    match step.direction:
        case Direction.Right:
            current_node = (current_node[0] + step.amount + 1, current_node[1])
        case Direction.Left:
            current_node = (current_node[0] - step.amount, current_node[1])
        case Direction.Up:
            current_node = (current_node[0], current_node[1] - step.amount)
        case Direction.Down:
            current_node = (current_node[0], current_node[1] + step.amount + 1)

    vertices.append(current_node)

print(vertices)
new_area = shoelace_area(vertices)
print(f"{new_area=}")


# normal [(0, 0), (6, 0), (6, 5), (4, 5), (4, 7), (6, 7), (6,  9), (1,  9), (1,  7), ( 0,  7), ( 0,  5), (2,  5), (2, 2), ( 0, 2), ( 0,  0)]
# + -    [(0, 0), (7, 0), (7, 6), (4, 6), (4, 9), (7, 9), (7, 12), (1, 12), (1,  9), (-1,  9), (-1,  6), (2,  6), (2, 2), (-1, 2), (-1, -1)]
# + +    [(0, 0), (7, 0), (7, 6), (6, 6), (6, 9), (9, 9), (9, 12), (5, 12), (5, 11), ( 5, 11), ( 5, 10), (8, 10), (8, 8), ( 7, 8), ( 7,  7)]
# goal   [(0, 0), (7, 0), (7, 6), (5, 6), (5, 7), (7, 7), (7, 10), (1, 10), (1,  8), ( 0,  8), ( 0,  5), (2,  5), (2, 3), ( 0, 3), ( 0,  0)]