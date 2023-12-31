from typing import NamedTuple

file_name = "input.txt"
with open(file_name) as file:
    lines = [line.rstrip() for line in file]

class Game(NamedTuple):
    id: int
    rounds: list[tuple[int, int, int]]

games: list[Game] = []
for line in lines:
    game_string, rounds = line.split(":")
    game_id = int(game_string.removeprefix("Game "))
    
    rounds_tuples: list[tuple[int, int, int]] = []
    round_list = rounds.split(";")
    for round in round_list:
        colors = round.split(",")

        red = 0
        green = 0
        blue = 0
        for color in colors:
            if "red" in color:
                red = int(color.replace("red", ""))
            elif "green" in color:
                green = int(color.replace("green", ""))
            elif "blue" in color:
                blue = int(color.replace("blue", ""))

        rounds_tuples.append((red, green, blue))

    games.append(Game(game_id, rounds_tuples))

MAX_RED_CUBES = 12
MAX_GREEN_CUBES = 13
MAX_BLUE_CUBES = 14

def check_game_possible(game: Game) -> bool:
    for round in game.rounds:
        if round[0] > MAX_RED_CUBES or round[1] > MAX_GREEN_CUBES or round[2] > MAX_BLUE_CUBES:
            return False

    return True

def get_games_score(games: list[Game]) -> int:
    final_score = 0
    for game in games:
        if check_game_possible(game):
            final_score += game.id

    return final_score

def min_game_colors_score(games: list[Game]) -> int:
    final_score = 0

    for game in games:
        min_red = 0
        min_green = 0
        min_blue = 0

        for round in game.rounds:
            if round[0] > min_red:
                min_red = round[0]
            if round[1] > min_green:
                min_green = round[1]
            if round[2] > min_blue:
                min_blue = round[2]

        final_score += min_red * min_green * min_blue

    return final_score

print(f"{get_games_score(games)=}")
print(f"{min_game_colors_score(games)=}")