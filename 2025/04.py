from utils.grid import Grid
from utils.point2d import Point2d

def silver_solution(lines: list[str]) -> int:
    grid = Grid[str](lines)
    
    rolls = set(grid.find_all_character_instances("@"))

    answer = 0

    for roll in rolls:
        valid = 0
        for neighbor in grid.get_neighbors(roll, True):
            if neighbor in rolls:
                valid += 1

        if valid < 4:
            answer += 1

    return answer

def gold_solution(lines: list[str]) -> int:
    grid = Grid[str](lines)

    answer = 0

    while True:
        rolls = set(grid.find_all_character_instances("@"))
        to_remove = set[Point2d]()
        for roll in rolls:
            valid = 0
            for neighbor in grid.get_neighbors(roll, True):
                if neighbor in rolls:
                    valid += 1

            if valid < 4:
                to_remove.add(roll)

        if len(to_remove) == 0:
            break

        answer += len(to_remove)
        for x in to_remove:
            grid.set_symbol(x, ".")
 
    return answer
