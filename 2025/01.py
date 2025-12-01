from utils.point2d import Direction2d

def parse_input(lines: list[str]) -> list[tuple[Direction2d, int]]:
    return [(Direction2d.from_character(line[0]), int(line[1:])) for line in lines if line]

def silver_solution(lines: list[str]) -> int:
    moves = parse_input(lines)

    current = 50
    result = 0

    for direction, movement in moves:
        if direction == Direction2d.LEFT:
            current -= movement
            while current < 0:
                current += 100
        elif direction == Direction2d.RIGHT:
            current += movement
            while current > 99:
                current -= 100
        
        if current == 0:
            result += 1

    return result

def gold_solution(lines: list[str]) -> int:
    moves = parse_input(lines)

    current = 50
    result = 0

    for direction, movement in moves:       
        if direction == Direction2d.LEFT:
            start = current
            moved = False
            current -= movement
            while current < 0:
                current += 100
                result += 1
                moved = True
            if current == 0:
                result += 1
            if moved and start == 0:
                result -= 1

        elif direction == Direction2d.RIGHT:
            current += movement
            while current > 99:
                current -= 100
                result += 1

    return result
