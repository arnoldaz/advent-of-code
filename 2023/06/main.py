from typing import NamedTuple

file_name = "input.txt"
with open(file_name) as file:
    lines = [line.rstrip() for line in file]

class Race(NamedTuple):
    time: int
    distance: int

def get_separate_races(lines: list[str]) -> list[Race]:
    races: list[Race] = []

    time_line = lines[0]
    distance_line = lines[1]
    _, time_number_string = time_line.split(":")
    _, distance_number_string = distance_line.split(":")
    time_numbers = [int(x) for x in time_number_string.split(" ") if x.strip() != ""]
    distance_numbers = [int(x) for x in distance_number_string.split(" ") if x.strip() != ""]
    for i in range(0, len(time_numbers)):
        races.append(Race(time_numbers[i], distance_numbers[i]))

    return races

def get_combined_race(lines: list[str]) -> Race:
    time_line = lines[0]
    distance_line = lines[1]
    _, time_number_string = time_line.split(":")
    _, distance_number_string = distance_line.split(":")
    time_number = int(time_number_string.replace(" ", ""))
    distance_number = int(distance_number_string.replace(" ", ""))

    return Race(time_number, distance_number)

def calculate_race_win_count(time: int, distance: int) -> int:
    final_count = 0

    for speed in range(1, time + 1):
        actual_time = time - speed
        traveled_distance = actual_time * speed
        if traveled_distance > distance:
            final_count += 1

    return final_count

def calculate_ways_to_win(races: list[Race]) -> int:
    final_count = 1

    for race in races:
        race_count = calculate_race_win_count(race.time, race.distance)
        final_count *= race_count

    return final_count

print(f"{calculate_ways_to_win(get_separate_races(lines))=}")
print(f"{calculate_ways_to_win([get_combined_race(lines)])=}")

