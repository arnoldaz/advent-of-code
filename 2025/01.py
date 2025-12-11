from utils.point2d import Direction2d

def parse_input(lines: list[str]) -> list[tuple[Direction2d, int]]:
    return [(Direction2d.from_character(line[0]), int(line[1:])) for line in lines]

def silver_solution(lines: list[str]) -> int:
    moves = parse_input(lines)
    position = 50
    answer = 0

    for direction, distance in moves:
        movement = -distance if direction == Direction2d.LEFT else distance
        position = (position + movement) % 100

        if position == 0:
            answer += 1

    return answer

def gold_solution(lines: list[str]) -> int:
    moves = parse_input(lines)
    position = 50
    answer = 0

    for direction, distance in moves:
        full_rotations, remainder = divmod(distance, 100)
        answer += full_rotations
        movement = -remainder if direction == Direction2d.LEFT else remainder
        next_position = position + movement

        if position != 0 and (next_position <= 0 or next_position >= 100):
            answer += 1

        position = next_position % 100

    return answer
