from typing import NamedTuple

class Game(NamedTuple):
    id: int
    rounds: list[tuple[int, int, int]]

def parse_input(lines: list[str]) -> list[Game]:
    games: list[Game] = []
    for line in lines:
        game_string, rounds = line.split(":")
        game_id = int(game_string.removeprefix("Game "))

        round_tuples: list[tuple[int, int, int]] = []
        for round_str in rounds.split(";"):
            rgb_values = { key: int(color.removesuffix(key)) for color in round_str.split(",") for key in ["red", "green", "blue"] if key in color }
            round_tuples.append((rgb_values.get("red", 0), rgb_values.get("green", 0), rgb_values.get("blue", 0)))

        games.append(Game(game_id, round_tuples))

    return games

def silver_solution(lines: list[str]) -> int:
    max_cubes = (12, 13, 14) # (red, green, blue)
    return sum(game.id for game in parse_input(lines) if all(round[i] <= max_cubes[i] for round in game.rounds for i in range(3)))

def gold_solution(lines: list[str]) -> int:
    final_score = 0
    for game in parse_input(lines):
        max_values = [max(color) for color in zip(*game.rounds)]
        final_score += max_values[0] * max_values[1] * max_values[2]

    return final_score
