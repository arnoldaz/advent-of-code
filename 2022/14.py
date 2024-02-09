import sys
from utils.matrix import Matrix
from utils.point import Direction, Point

WALL_SYMBOL = 1
SAND_SYMBOL = 2

# Safe assumptions by how much to increase initial matrix for incoming sand
LEEWAY_TILE_COUNT = {
    Direction.UP: 50,
    Direction.DOWN: 5,
    Direction.LEFT: 200,
    Direction.RIGHT: 200,
}

def parse_input(lines: list[str], add_ground: bool) -> tuple[Matrix[int], Point]:
    map_lines: list[tuple[Point, Point]] = []

    for line in lines:
        corners = [Point(int(x), int(y)) for corner_pair in line.split(" -> ") for x, y in [corner.split(",") for corner in corner_pair.split()]]
        for corner1, corner2 in zip(corners, corners[1:]):
            if corner1.x == corner2.x:
                map_lines.append((Point(corner1.x, min(corner1.y, corner2.y)), Point(corner1.x, max(corner1.y, corner2.y))))
            elif corner1.y == corner2.y:
                map_lines.append((Point(min(corner1.x, corner2.x), corner1.y), Point(max(corner1.x, corner2.x), corner1.y)))
            else:
                raise ValueError("Impossible input")

    max_x, max_y, min_x, min_y = 0, 0, sys.maxsize, sys.maxsize
    for start, end in map_lines:
        min_x = min(min_x, start.x, end.x)
        max_x = max(max_x, start.x, end.x)
        min_y = min(min_y, start.y, end.y)
        max_y = max(max_y, start.y, end.y)

    width = max_x - min_x + LEEWAY_TILE_COUNT[Direction.LEFT] + LEEWAY_TILE_COUNT[Direction.RIGHT]
    height = max_y - min_y + LEEWAY_TILE_COUNT[Direction.UP] + LEEWAY_TILE_COUNT[Direction.DOWN]
    data = [[0 for _ in range(width)] for _ in range(height)]
    offset = Point(min_x - LEEWAY_TILE_COUNT[Direction.LEFT], min_y - LEEWAY_TILE_COUNT[Direction.UP])

    for start, end in map_lines:
        if start.x == end.x:
            for y in range(min(start.y, end.y), max(start.y, end.y) + 1):
                data[y - offset.y][start.x - offset.x] = WALL_SYMBOL
        elif start.y == end.y:
            for x in range(min(start.x, end.x), max(start.x, end.x) + 1):
                data[start.y - offset.y][x - offset.x] = WALL_SYMBOL
        else:
            raise ValueError("Impossible input")

    if add_ground:
        for x in range(width):
            data[max_y + 2 - offset.y][x] = WALL_SYMBOL

    return Matrix[int](data, int), offset

def drop_sand(matrix: Matrix[int], sand_start: Point, offset: Point) -> bool:
    sand_start -= offset
    if matrix.get_symbol(sand_start) == SAND_SYMBOL:
        return False

    column = matrix.get_column(sand_start.x)
    first_obstacle_y = next((i for i, value in enumerate(column) if value > 0 and i > sand_start.y), None)
    if first_obstacle_y is None:
        return False

    first_obstacle = Point(sand_start.x, first_obstacle_y)

    obstacle_left = first_obstacle + Direction.LEFT
    if matrix.get_symbol(obstacle_left) == 0:
        return drop_sand(matrix, obstacle_left, Point())

    obstacle_right = first_obstacle + Direction.RIGHT
    if matrix.get_symbol(obstacle_right) == 0:
        return drop_sand(matrix, obstacle_right, Point())

    matrix.set_symbol(first_obstacle + Direction.UP, SAND_SYMBOL)
    return True

def calculate_sand_amount(matrix: Matrix[int], offset: Point) -> int:
    sand_start = Point(500, 0)
    while drop_sand(matrix, sand_start, offset):
        pass

    # visualize_matrix(matrix)
    return sum(number == SAND_SYMBOL for line in matrix.get_data() for number in line)

def visualize_matrix(matrix: Matrix[int]):
    # pylint: disable-next=import-outside-toplevel
    from colorama import Fore

    height, width = matrix.height(), matrix.width()
    for y in range(height):
        for x in range(width):
            symbol = matrix.get_symbol(Point(x, y))
            if symbol == WALL_SYMBOL:
                print(f"{Fore.BLUE}0{Fore.RESET}", end="")
            elif symbol == SAND_SYMBOL:
                print(f"{Fore.RED}0{Fore.RESET}", end="")
            else:
                print("0", end="")
        print()

def silver_solution(lines: list[str]) -> int:
    matrix, offset = parse_input(lines, False)
    return calculate_sand_amount(matrix, offset)

def gold_solution(lines: list[str]) -> int:
    matrix, offset = parse_input(lines, True)
    return calculate_sand_amount(matrix, offset)
