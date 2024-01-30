from typing import NamedTuple

class Round(NamedTuple):
    opponent_move: str
    my_move: str

def parse_rounds(lines: list[str]) -> list[Round]:
    rounds: list[Round] = []
    for line in lines:
        opponent_move, my_move = line.split(" ")
        rounds.append(Round(opponent_move, my_move))

    return rounds

SILVER_MOVE_CONVERSION = {
    "X": "A",
    "Y": "B",
    "Z": "C",
}

MOVE_SCORE = {
    "A": 1,
    "B": 2,
    "C": 3,
}

def get_round_outcome_score(opponent_move: str, my_move: str) -> int:
    # 0 for defeat, 3 for draw, 6 for win
    # A for rock, B for paper, C for scissors
    if opponent_move == my_move:
        return 3

    match opponent_move:
        case "A": # rock
            return 6 if my_move == "B" else 0
        case "B": # paper
            return 6 if my_move == "C" else 0
        case "C": # scissors
            return 6 if my_move == "A" else 0
        case _: # impossible to reach
            return -99999

def silver_solution(lines: list[str]) -> int:
    game_rounds = parse_rounds(lines)
    score = 0

    for game_round in game_rounds:
        opponent_move, my_move = game_round.opponent_move, SILVER_MOVE_CONVERSION[game_round.my_move]
        outcome_score = get_round_outcome_score(opponent_move, my_move)
        response_score = MOVE_SCORE[my_move]
        score += outcome_score + response_score

    return score

LOSING_MOVE_CONVERSION = {
    "A": "C",
    "B": "A",
    "C": "B",
}

WINNING_MOVE_CONVERSION = {
    "A": "B",
    "B": "C",
    "C": "A",
}

def gold_solution(lines: list[str]) -> int:
    game_rounds = parse_rounds(lines)
    score = 0

    for game_round in game_rounds:
        match game_round.my_move:
            case "X": # lose
                my_real_move = LOSING_MOVE_CONVERSION[game_round.opponent_move]
                outcome_score = 0
            case "Y": # draw
                my_real_move = game_round.opponent_move
                outcome_score = 3
            case "Z": # win
                my_real_move = WINNING_MOVE_CONVERSION[game_round.opponent_move]
                outcome_score = 6
            case _: # impossible to reach
                my_real_move = "AAAAA"
                outcome_score = -99999

        response_score = MOVE_SCORE[my_real_move]
        score += outcome_score + response_score

    return score
