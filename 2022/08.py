from utils.matrix import Matrix
from utils.point import Point

def is_tree_visible(forest: Matrix[int], location: Point) -> bool:
    tree_height = forest.get_symbol(location) or -1
    row = forest.get_row(location.y) or []
    column = forest.get_column(location.x) or []

    if all(x < tree_height for x in row[:location.x]): # left
        return True

    if all(x < tree_height for x in row[location.x+1:]): # right
        return True

    if all(x < tree_height for x in column[:location.y]): # up
        return True

    if all(x < tree_height for x in column[location.y+1:]): # down
        return True

    return False

def count_visible_trees(forest: Matrix[int], location: Point) -> int:
    tree_height = forest.get_symbol(location) or -1
    row = forest.get_row(location.y) or []
    column = forest.get_column(location.x) or []

    left_trees = row[:location.x]
    left_visible = next((i + 1 for i, x in enumerate(reversed(left_trees)) if x >= tree_height), len(left_trees))

    right_trees = row[location.x+1:]
    right_visible = next((i + 1 for i, x in enumerate(right_trees) if x >= tree_height), len(right_trees))

    up_trees = column[:location.y]
    up_visible = next((i + 1 for i, x in enumerate(reversed(up_trees)) if x >= tree_height), len(up_trees))

    down_trees = column[location.y+1:]
    down_visible = next((i + 1 for i, x in enumerate(down_trees) if x >= tree_height), len(down_trees))

    return left_visible * right_visible * up_visible * down_visible

def silver_solution(lines: list[str]) -> int:
    forest = Matrix[int](lines, int)
    return sum(1 for y, row in enumerate(forest.get_data()) for x, _ in enumerate(row) if is_tree_visible(forest, Point(x, y)))

def gold_solution(lines: list[str]) -> int:
    forest = Matrix[int](lines, int)
    return max(count_visible_trees(forest, Point(x, y)) for y, row in enumerate(forest.get_data()[1:-1]) for x, _ in enumerate(row[1:-1]))
