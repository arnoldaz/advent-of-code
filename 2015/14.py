from typing import NamedTuple

class Reindeer(NamedTuple):
    name: str
    speed: int
    time: int
    rest: int

def parse_input(lines: list[str]) -> list[Reindeer]:
    return [
        Reindeer(words[0], int(words[3]), int(words[6]), int(words[13]))
        for line in lines
        if (words := line.split())
    ]

def silver_solution(lines: list[str]) -> int:
    reindeers = parse_input(lines)

    max_distance = 0
    for reindeer in reindeers:
        full, leftover = divmod(2503, reindeer.time + reindeer.rest)
        total = full * reindeer.speed * reindeer.time
        total += reindeer.speed * min(leftover, reindeer.time)
        max_distance = max(max_distance, total)

    return max_distance

def gold_solution(lines: list[str]) -> int:
    reindeers = parse_input(lines)

    scores = {reindeer.name: 0 for reindeer in reindeers}
    distances_traveled = {reindeer.name: 0 for reindeer in reindeers}

    for i in range(1, 2503 + 1):
        for reindeer in reindeers:
            if 0 < i % (reindeer.time + reindeer.rest) <= reindeer.time:
                distances_traveled[reindeer.name] += reindeer.speed

        max_value = max(distances_traveled.values())
        for name in (name for name, value in distances_traveled.items() if value == max_value):
            scores[name] += 1

    return max(scores.values())
