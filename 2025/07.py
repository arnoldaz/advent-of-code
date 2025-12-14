from functools import cache
from utils.grid import Grid
from utils.point2d import Point2d

def silver_solution(lines: list[str]) -> int:
    grid = Grid[str](lines)
    split_count = 0

    beams = {grid.find_first_character_instance("S")}
    splitters = set(grid.find_all_character_instances("^"))

    running = True
    while running:
        beams = set(Point2d(beam.x, beam.y+1) for beam in beams)
        for beam in beams.copy():
            if not grid.in_bounds(beam):
                running = False
                break

            if beam in splitters:
                split_count += 1
                beams -= {beam}
                beams |= {Point2d(beam.x-1, beam.y), Point2d(beam.x+1, beam.y)}

    return split_count

def get_timelines(beam: Point2d, splitters: set[Point2d], height: int) -> int:
    @cache
    def get_timelines_recursive(beam: Point2d) -> int:
        new_beam = Point2d(beam.x, beam.y+1)
        if new_beam.y >= height:
            return 1

        if new_beam in splitters:
            return get_timelines_recursive(Point2d(new_beam.x-1, new_beam.y)) + get_timelines_recursive(Point2d(new_beam.x+1, new_beam.y))

        return get_timelines_recursive(new_beam)

    return get_timelines_recursive(beam)

def gold_solution(lines: list[str]) -> int:
    grid = Grid[str](lines)
    beam = grid.find_first_character_instance("S")
    splitters = set(grid.find_all_character_instances("^"))

    return get_timelines(beam, splitters, grid.height())
