from enum import Enum

with open("input.txt") as file:
    lines = [line.rstrip() for line in file]

class Direction(Enum):
    No = (0, 0)
    Up = (0, -1)
    Right = (1, 0)
    Down = (0, 1)
    Left = (-1, 0)

starting_position = (-1, -1)

outer_break = False
for y, line in enumerate(lines):
    for x, char in enumerate(line):
        if char == "S":
            starting_position = (x, y)
            outer_break = True
            break
    if outer_break:
        break

def debug_print_grid(positions: list[tuple[int, int]], grid: list[str]):
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if (x, y) in positions:
                print("O", end="")
            else:
                print(char if char != "S" else ".", end="")  
        print()

def is_in_bounds(position: tuple[int, int], grid: list[str]):
    height = len(grid)
    width = len(grid[0])
    
    x, y = position
    
    return 0 <= x < width and 0 <= y < height

def calculate_possible_positions(starting_position: tuple[int, int], grid: list[str], max_iterations: int):
    current_positions = [starting_position]
    
    iterations = 0
    while iterations < max_iterations:
        iterations += 1
        
        new_positions = []
        for current_position in current_positions:
            up = tuple[int, int]([sum(x) for x in zip(current_position, Direction.Up.value)])
            down = tuple[int, int]([sum(x) for x in zip(current_position, Direction.Down.value)])
            left = tuple[int, int]([sum(x) for x in zip(current_position, Direction.Left.value)])
            right = tuple[int, int]([sum(x) for x in zip(current_position, Direction.Right.value)])

            if is_in_bounds(up, grid) and grid[up[1]][up[0]] != "#":
                new_positions.append(up)
            if is_in_bounds(down, grid) and grid[down[1]][down[0]] != "#":
                new_positions.append(down)
            if is_in_bounds(left, grid) and grid[left[1]][left[0]] != "#":
                new_positions.append(left)
            if is_in_bounds(right, grid) and grid[right[1]][right[0]] != "#":
                new_positions.append(right)

        current_positions = list(set(new_positions))
    
    
    print(f"====== iteration {iterations}")
    debug_print_grid(current_positions, grid)
    print("======")
    return len(current_positions)
    
                


print(f"{calculate_possible_positions(starting_position, lines, 1000)=}")