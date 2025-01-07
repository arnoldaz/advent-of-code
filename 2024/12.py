from utils.matrix import Matrix
from utils.point import Direction, Point

# TODO

def flood_fill(grid: Matrix[str], location: Point, original_symbol: str, filled_points: list[Point]):
    if location in filled_points:
        return

    if grid.get_symbol(location) != original_symbol:
        return

    filled_points.append(location)
    for neighbor, _ in grid.get_neighbors(location):
        flood_fill(grid, neighbor, original_symbol, filled_points)

def silver_solution(lines: list[str]) -> int:
    grid = Matrix[str](lines, str)

    groups: list[list[Point]] = []

    for y in range(grid.height()):
        for x in range(grid.width()):
            point = Point(x, y)

            in_group = False
            for group in groups:
                if point in group:
                    in_group = True
                    break

            if in_group:
                continue

            symbol = grid.get_symbol(point)

            filled_points = list[Point]()
            flood_fill(grid, point, symbol, filled_points)
            groups.append(filled_points)

    result = 0

    for group in groups:
        area = len(group)
        perimeter = 0

        for y in range(grid.height()):
            for x in range(grid.width()):
                point = Point(x, y)
                if point not in group:
                    continue

                perimeter += 4

                if point + Direction.UP in group:
                    perimeter -= 2

                if point + Direction.LEFT in group:
                    perimeter -= 2

        # print(area, perimeter)
        result += area * perimeter

    return result

def get_next_direction(dir: Direction) -> Direction:
    match dir:
        case Direction.UP:
            return Direction.RIGHT
        case Direction.RIGHT:
            return Direction.DOWN
        case Direction.DOWN:
            return Direction.LEFT
        case Direction.LEFT:
            return Direction.UP
        
    return Direction.NONE

def gold_solution(lines: list[str]) -> int:
    grid = Matrix[str](lines, str)

    groups: list[list[Point]] = []

    for y in range(grid.height()):
        for x in range(grid.width()):
            point = Point(x, y)

            in_group = False
            for group in groups:
                if point in group:
                    in_group = True
                    break

            if in_group:
                continue

            symbol = grid.get_symbol(point)

            filled_points = list[Point]()
            flood_fill(grid, point, symbol, filled_points)
            groups.append(filled_points)

    result = 0

    # grid.print(1)

    for group in groups:
        up_walls: list[Point] = []
        down_walls: list[Point] = []
        left_walls: list[Point] = []
        right_walls: list[Point] = []

        for element in group:
            if element + Direction.UP not in group:
                up_walls.append(element)
            if element + Direction.DOWN not in group:
                down_walls.append(element)
            if element + Direction.LEFT not in group:
                left_walls.append(element)
            if element + Direction.RIGHT not in group:
                right_walls.append(element)

        up_walls.sort(key=lambda wall: (wall.y, wall.x))
        down_walls.sort(key=lambda wall: (wall.y, wall.x))
        left_walls.sort(key=lambda wall: (wall.x, wall.y))
        right_walls.sort(key=lambda wall: (wall.x, wall.y))

        up_line_count = 0
        for i, wall in enumerate(up_walls):
            if i == 0:
                up_line_count += 1
                continue

            previous_wall = up_walls[i-1]
            if wall.y == previous_wall.y and wall.x - 1 == previous_wall.x:
                pass
            else:
                up_line_count += 1

        down_line_count = 0
        for i, wall in enumerate(down_walls):
            if i == 0:
                down_line_count += 1
                continue

            previous_wall = down_walls[i-1]
            if wall.y == previous_wall.y and wall.x - 1 == previous_wall.x:
                pass
            else:
                down_line_count += 1

        left_line_count = 0
        for i, wall in enumerate(left_walls):
            if i == 0:
                left_line_count += 1
                continue

            previous_wall = left_walls[i-1]
            if wall.x == previous_wall.x and wall.y - 1 == previous_wall.y:
                pass
            else:
                left_line_count += 1

        right_line_count = 0
        for i, wall in enumerate(right_walls):
            if i == 0:
                right_line_count += 1
                continue

            previous_wall = right_walls[i-1]
            if wall.x == previous_wall.x and wall.y - 1 == previous_wall.y:
                pass
            else:
                right_line_count += 1

        line_count = up_line_count + down_line_count + left_line_count + right_line_count
        area = len(group)

        # print(area, line_count)

        result += area * line_count

        # print(group)
        # print(up_line_count)
        # print(down_line_count)
        # print(left_line_count)
        # print(right_line_count)
        # print("---")
        # print(up_walls)
        # print(down_walls)
        # print(left_walls)
        # print(right_walls)
        # print("---===================================")

    return result
