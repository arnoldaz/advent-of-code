from utils.grid import Grid

def silver_solution(lines: list[str]) -> int:
    grid = Grid[str](lines)
    rolls = set(grid.find_all_character_instances("@"))
    neighbors_map = {roll: set(grid.get_neighbors(roll, True)) for roll in rolls}

    return sum(1 for roll in rolls if len(neighbors_map[roll] & rolls) < 4)

def gold_solution(lines: list[str]) -> int:
    grid = Grid[str](lines)
    rolls = set(grid.find_all_character_instances("@"))
    neighbors_map = {roll: set(grid.get_neighbors(roll, True)) for roll in rolls}

    answer = 0
    while rolls_to_remove := {roll for roll in rolls if len(neighbors_map[roll] & rolls) < 4}:
        answer += len(rolls_to_remove)
        rolls -= rolls_to_remove

    return answer
