from functools import reduce
import math
from typing import NamedTuple

class Race(NamedTuple):
    time: int
    distance: int

def get_separate_races(lines: list[str]) -> list[Race]:
    time_line, distance_line = lines[0], lines[1]
    time_numbers = [int(x) for x in time_line.split(":")[1].split() if x.strip()]
    distance_numbers = [int(x) for x in distance_line.split(":")[1].split() if x.strip()]

    return [Race(time_numbers[i], distance_numbers[i]) for i in range(len(time_numbers))]

def get_combined_race(lines: list[str]) -> Race:
    time_line, distance_line = lines[0], lines[1]
    time_number = int(time_line.split(":")[1].replace(" ", ""))
    distance_number = int(distance_line.split(":")[1].replace(" ", ""))

    return Race(time_number, distance_number)

def calculate_race_win_count(time: int, distance: int) -> int:
    discriminant = time * time - 4 * distance
    x1 = (-time + math.sqrt(discriminant)) / (-2)
    x2 = (-time - math.sqrt(discriminant)) / (-2)

    solution_range = x2 - x1

    return int(solution_range) - 1 if solution_range.is_integer() else math.floor(x2) - math.ceil(x1) + 1

def calculate_ways_to_win(races: list[Race]) -> int:
    return reduce(lambda x, race: x * calculate_race_win_count(race.time, race.distance), races, 1)

def silver_solution(lines: list[str]) -> int:
    return calculate_ways_to_win(get_separate_races(lines))

def gold_solution(lines: list[str]) -> int:
    return calculate_ways_to_win([get_combined_race(lines)])
