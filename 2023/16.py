from enum import Enum

class Direction(Enum):
    No = 0
    Up = 1
    Right = 2
    Down = 3
    Left = 4

def debug_print_energized_map(energized_map: list[list[list[Direction]]]):
    energized_visualization = [["."] * len(energized_map[0]) for _ in range(len(energized_map))]

    for i, energized_line in enumerate(energized_map):
        for j, energized_tile in enumerate(energized_line):
            if len(energized_tile) > 0:
                energized_visualization[i][j] = "#"

    print("======================================")

    for energized_line in energized_visualization:
        for energized_tile in energized_line:
            print(energized_tile, end="")
        print()

    print("======================================")

def calculate_energized_tiles(lines: list[str]) -> int:
    energized_map: list[list[list[Direction]]] = [[[] for _ in range(len(lines[0]))] for _ in range(len(lines))]
    beams: list[tuple[int, int, Direction]] = [(-1, 0, Direction.Right)]
    delete_beams: list[int] = []

    while len(beams) > 0:
        for i, beam in enumerate(beams[:]):
            direction = beam[2]
            match direction:
                case Direction.Up:
                    next_location = (beam[0], beam[1]-1)
                case Direction.Right:
                    next_location = (beam[0]+1, beam[1])
                case Direction.Down:
                    next_location = (beam[0], beam[1]+1)
                case Direction.Left:
                    next_location = (beam[0]-1, beam[1])
                case _:
                    next_location = (beam[0], beam[1]) # impossible

            if next_location[0] < 0 or next_location[0] >= len(lines[0]) or next_location[1] < 0 or next_location[1] >= len(lines):
                delete_beams.append(i)
                continue

            if direction in energized_map[next_location[1]][next_location[0]]:
                delete_beams.append(i)
                continue

            energized_map[next_location[1]][next_location[0]].append(direction)
            next_symbol = lines[next_location[1]][next_location[0]]

            match next_symbol:
                case ".":
                    beams[i] = (next_location[0], next_location[1], direction)
                case "|" if direction == Direction.Up or direction == Direction.Down:
                    beams[i] = (next_location[0], next_location[1], direction)
                case "|" if direction == Direction.Left or direction == Direction.Right:
                    delete_beams.append(i)
                    beams.append((next_location[0], next_location[1], Direction.Up))
                    beams.append((next_location[0], next_location[1], Direction.Down))
                case "-" if direction == Direction.Left or direction == Direction.Right:
                    beams[i] = (next_location[0], next_location[1], direction)
                case "-" if direction == Direction.Up or direction == Direction.Down:
                    delete_beams.append(i)
                    beams.append((next_location[0], next_location[1], Direction.Left))
                    beams.append((next_location[0], next_location[1], Direction.Right))
                case "\\" if direction == Direction.Left:
                    beams[i] = (next_location[0], next_location[1], Direction.Up)
                case "\\" if direction == Direction.Up:
                    beams[i] = (next_location[0], next_location[1], Direction.Left)
                case "\\" if direction == Direction.Right:
                    beams[i] = (next_location[0], next_location[1], Direction.Down)
                case "\\" if direction == Direction.Down:
                    beams[i] = (next_location[0], next_location[1], Direction.Right)
                case "/" if direction == Direction.Left:
                    beams[i] = (next_location[0], next_location[1], Direction.Down)
                case "/" if direction == Direction.Up:
                    beams[i] = (next_location[0], next_location[1], Direction.Right)
                case "/" if direction == Direction.Right:
                    beams[i] = (next_location[0], next_location[1], Direction.Up)
                case "/" if direction == Direction.Down:
                    beams[i] = (next_location[0], next_location[1], Direction.Left)

        delete_beams.reverse()
        for delete_beam in delete_beams:
            beams.pop(delete_beam)
        delete_beams = []

    final_result = 0

    for i, energized_line in enumerate(energized_map):
        for energized_tile in energized_line:
            if len(energized_tile) > 0:
                final_result += 1

    return final_result

def calculate_energized_tiles_all_edges(lines: list[str]) -> int:
    results: list[int] = []
    all_possible_starts: list[tuple[int, int, Direction]] = []

    x_length = len(lines[0])
    y_length = len(lines)

    for i in range(x_length):
        all_possible_starts.append((i, -1, Direction.Down))
        all_possible_starts.append((i, y_length, Direction.Up))

    for i in range(y_length):
        all_possible_starts.append((-1, i, Direction.Right))
        all_possible_starts.append((x_length, i, Direction.Left))

    for possible_start in all_possible_starts:
        energized_map: list[list[list[Direction]]] = [[[] for _ in range(x_length)] for _ in range(y_length)]
        beams: list[tuple[int, int, Direction]] = [possible_start]
        delete_beams: list[int] = []

        while len(beams) > 0:
            for i, beam in enumerate(beams[:]):
                direction = beam[2]
                match direction:
                    case Direction.Up:
                        next_location = (beam[0], beam[1]-1)
                    case Direction.Right:
                        next_location = (beam[0]+1, beam[1])
                    case Direction.Down:
                        next_location = (beam[0], beam[1]+1)
                    case Direction.Left:
                        next_location = (beam[0]-1, beam[1])
                    case _:
                        next_location = (beam[0], beam[1]) # impossible

                if next_location[0] < 0 or next_location[0] >= x_length or next_location[1] < 0 or next_location[1] >= y_length:
                    delete_beams.append(i)
                    continue

                if direction in energized_map[next_location[1]][next_location[0]]:
                    delete_beams.append(i)
                    continue

                energized_map[next_location[1]][next_location[0]].append(direction)
                next_symbol = lines[next_location[1]][next_location[0]]

                match next_symbol:
                    case ".":
                        beams[i] = (next_location[0], next_location[1], direction)
                    case "|" if direction == Direction.Up or direction == Direction.Down:
                        beams[i] = (next_location[0], next_location[1], direction)
                    case "|" if direction == Direction.Left or direction == Direction.Right:
                        delete_beams.append(i)
                        beams.append((next_location[0], next_location[1], Direction.Up))
                        beams.append((next_location[0], next_location[1], Direction.Down))
                    case "-" if direction == Direction.Left or direction == Direction.Right:
                        beams[i] = (next_location[0], next_location[1], direction)
                    case "-" if direction == Direction.Up or direction == Direction.Down:
                        delete_beams.append(i)
                        beams.append((next_location[0], next_location[1], Direction.Left))
                        beams.append((next_location[0], next_location[1], Direction.Right))
                    case "\\" if direction == Direction.Left:
                        beams[i] = (next_location[0], next_location[1], Direction.Up)
                    case "\\" if direction == Direction.Up:
                        beams[i] = (next_location[0], next_location[1], Direction.Left)
                    case "\\" if direction == Direction.Right:
                        beams[i] = (next_location[0], next_location[1], Direction.Down)
                    case "\\" if direction == Direction.Down:
                        beams[i] = (next_location[0], next_location[1], Direction.Right)
                    case "/" if direction == Direction.Left:
                        beams[i] = (next_location[0], next_location[1], Direction.Down)
                    case "/" if direction == Direction.Up:
                        beams[i] = (next_location[0], next_location[1], Direction.Right)
                    case "/" if direction == Direction.Right:
                        beams[i] = (next_location[0], next_location[1], Direction.Up)
                    case "/" if direction == Direction.Down:
                        beams[i] = (next_location[0], next_location[1], Direction.Left)

            delete_beams.reverse()
            for delete_beam in delete_beams:
                beams.pop(delete_beam)
            delete_beams = []

        final_result = 0

        for i, energized_line in enumerate(energized_map):
            for energized_tile in energized_line:
                if len(energized_tile) > 0:
                    final_result += 1

        results.append(final_result)

    return max(results)

def silver_solution(lines: list[str]) -> int:
    return calculate_energized_tiles(lines)

def gold_solution(lines: list[str]) -> int:
    return calculate_energized_tiles_all_edges(lines)
