from utils.list import remove_list_indexes
from utils.matrix import Matrix
from utils.point import Direction, Point

def calculate_energized_tiles(tile_map: Matrix[str], starting_location: tuple[Point, Direction]) -> int:
    height, width = tile_map.height(), tile_map.width()
    energized_map: list[list[list[Direction]]] = [[[] for _ in range(width)] for _ in range(height)]
    beams: list[tuple[Point, Direction]] = [starting_location]
    delete_beams: list[int] = []

    while len(beams) > 0:
        for i, (beam_location, beam_direction) in enumerate(beams[:]):
            next_location = beam_location + beam_direction

            if not tile_map.in_bounds(next_location):
                delete_beams.append(i)
                continue

            if beam_direction in energized_map[next_location.y][next_location.x]:
                delete_beams.append(i)
                continue

            energized_map[next_location.y][next_location.x].append(beam_direction)
            next_symbol = tile_map.get_symbol(next_location)

            match next_symbol:
                case ".":
                    beams[i] = (next_location, beam_direction)
                case "|" if beam_direction in (Direction.UP, Direction.DOWN):
                    beams[i] = (next_location, beam_direction)
                case "|" if beam_direction in (Direction.LEFT, Direction.RIGHT):
                    delete_beams.append(i)
                    beams.append((next_location, Direction.UP))
                    beams.append((next_location, Direction.DOWN))
                case "-" if beam_direction in (Direction.LEFT, Direction.RIGHT):
                    beams[i] = (next_location, beam_direction)
                case "-" if beam_direction in (Direction.UP, Direction.DOWN):
                    delete_beams.append(i)
                    beams.append((next_location, Direction.LEFT))
                    beams.append((next_location, Direction.RIGHT))
                case "\\" if beam_direction == Direction.LEFT:
                    beams[i] = (next_location, Direction.UP)
                case "\\" if beam_direction == Direction.UP:
                    beams[i] = (next_location, Direction.LEFT)
                case "\\" if beam_direction == Direction.RIGHT:
                    beams[i] = (next_location, Direction.DOWN)
                case "\\" if beam_direction == Direction.DOWN:
                    beams[i] = (next_location, Direction.RIGHT)
                case "/" if beam_direction == Direction.LEFT:
                    beams[i] = (next_location, Direction.DOWN)
                case "/" if beam_direction == Direction.UP:
                    beams[i] = (next_location, Direction.RIGHT)
                case "/" if beam_direction == Direction.RIGHT:
                    beams[i] = (next_location, Direction.UP)
                case "/" if beam_direction == Direction.DOWN:
                    beams[i] = (next_location, Direction.LEFT)

        remove_list_indexes(beams, delete_beams)
        delete_beams = []

    return sum(1 for energized_line in energized_map for energized_tile in energized_line if len(energized_tile) > 0)

def calculate_energized_tiles_all_edges(tile_map: Matrix[str]) -> int:
    height, width = tile_map.height(), tile_map.width()
    all_possible_starts: list[tuple[Point, Direction]] = []

    for i in range(width):
        all_possible_starts.append((Point(i, -1), Direction.DOWN))
        all_possible_starts.append((Point(i, height), Direction.UP))

    for i in range(height):
        all_possible_starts.append((Point(-1, i), Direction.RIGHT))
        all_possible_starts.append((Point(width, i), Direction.LEFT))

    return max(calculate_energized_tiles(tile_map, possible_start) for possible_start in all_possible_starts)

def silver_solution(lines: list[str]) -> int:
    tile_map = Matrix[str](lines, str)
    return calculate_energized_tiles(tile_map, (Point(-1, 0), Direction.RIGHT))

def gold_solution(lines: list[str]) -> int:
    tile_map = Matrix[str](lines, str)
    return calculate_energized_tiles_all_edges(tile_map)
