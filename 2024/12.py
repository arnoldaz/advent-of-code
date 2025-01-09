from utils.grid import Grid
from utils.point2d import Direction2d, Point2d

def flood_fill(grid: Grid[str], location: Point2d, original_symbol: str, filled_points: set[Point2d]):
    if location in filled_points:
        return

    if grid.get_symbol(location) != original_symbol:
        return

    filled_points.add(location)
    for neighbor in grid.get_neighbors(location):
        flood_fill(grid, neighbor, original_symbol, filled_points)

def get_groups(grid: Grid[str]):
    groups: list[set[Point2d]] = []

    for point, symbol in grid.iterate():
        if any(point in group for group in groups):
            continue

        filled_points = set[Point2d]()
        flood_fill(grid, point, symbol, filled_points)
        groups.append(filled_points)

    return groups

def get_side_line_count(walls: list[Point2d], is_horizontal_side: bool):
    line_count = 0
    for i, wall in enumerate(walls):
        if i == 0:
            line_count += 1
            continue

        previous_wall = walls[i-1]

        if is_horizontal_side:
            is_same_line = wall.y == previous_wall.y and wall.x - 1 == previous_wall.x
        else:
            is_same_line = wall.x == previous_wall.x and wall.y - 1 == previous_wall.y

        if not is_same_line:
            line_count += 1

    return line_count

def silver_solution(lines: list[str]) -> int:
    grid = Grid[str](lines)

    groups = get_groups(grid)
    total_price = 0

    for group in groups:
        area = len(group)
        perimeter = 0

        for point in group:
            for neighbor in point.get_neighbors_no_bounds():
                if not grid.in_bounds(neighbor) or grid.get_symbol(neighbor) != grid.get_symbol(point):
                    perimeter += 1

        total_price += area * perimeter

    return total_price

def gold_solution(lines: list[str]) -> int:
    grid = Grid[str](lines)

    groups = get_groups(grid)
    total_price = 0

    for group in groups:
        up_walls: list[Point2d] = []
        down_walls: list[Point2d] = []
        left_walls: list[Point2d] = []
        right_walls: list[Point2d] = []

        for element in group:
            if element + Direction2d.UP not in group:
                up_walls.append(element)
            if element + Direction2d.DOWN not in group:
                down_walls.append(element)
            if element + Direction2d.LEFT not in group:
                left_walls.append(element)
            if element + Direction2d.RIGHT not in group:
                right_walls.append(element)

        up_walls.sort(key=lambda wall: (wall.y, wall.x))
        down_walls.sort(key=lambda wall: (wall.y, wall.x))
        left_walls.sort(key=lambda wall: (wall.x, wall.y))
        right_walls.sort(key=lambda wall: (wall.x, wall.y))

        up_line_count = get_side_line_count(up_walls, True)
        down_line_count = get_side_line_count(down_walls, True)
        left_line_count = get_side_line_count(left_walls, False)
        right_line_count = get_side_line_count(right_walls, False)

        line_count = up_line_count + down_line_count + left_line_count + right_line_count
        area = len(group)

        total_price += area * line_count

    return total_price
