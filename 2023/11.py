from utils.point import Point

def get_expanded_indexes(lines: list[str]) -> tuple[list[int], list[int]]:
    empty_rows: list[int] = []
    empty_columns: list[int] = []

    for i, line in enumerate(lines):
        if all(char == "." for char in line):
            empty_rows.append(i)

    for i in range(len(lines[0])):
        if all(char == "." for char in [line[i] for line in lines]):
            empty_columns.append(i)

    return empty_rows, empty_columns

def get_star_distance1(star1: Point, star2: Point, empty_rows: list[int], empty_columns: list[int], empty_expansion_amount: int) -> int:
    x_diff = abs(star1.x - star2.x) + sum(empty_expansion_amount - 1 for column in empty_columns if star1.x > column > star2.x or star1.x < column < star2.x)
    y_diff = abs(star1.y - star2.y) + sum(empty_expansion_amount - 1 for row in empty_rows if star1.y > row > star2.y or star1.y < row < star2.y)

    return x_diff + y_diff

def get_star_distance2(star1: Point, star2: Point, empty_rows: list[int], empty_columns: list[int], empty_expansion_amount: int) -> int:
    star_first_x = star1.x if star1.x >= star2.x else star2.x
    star_second_x = star2.x if star1.x >= star2.x else star1.x

    star_first_y = star1.y if star1.y >= star2.y else star2.y
    star_second_y = star2.y if star1.y >= star2.y else star1.y

    x_diff = star_first_x - star_second_x
    y_diff = star_first_y - star_second_y

    for column in empty_columns:
        if star_first_x > column > star_second_x:
            x_diff += empty_expansion_amount - 1

    for row in empty_rows:
        if star_first_y > row > star_second_y:
            y_diff += empty_expansion_amount - 1

    return x_diff + y_diff

def get_star_distance3(star1: Point, star2: Point, empty_rows: list[int], empty_columns: list[int], empty_expansion_amount: int) -> int:
    star_first_x, star_second_x = (star1.x, star2.x) if star1.x > star2.x else (star2.x, star1.x)
    star_first_y, star_second_y = (star1.y, star2.y) if star1.y > star2.y else (star2.y, star1.y)

    diff = star_first_x - star_second_x + star_first_y - star_second_y

    count = 0
    for column in empty_columns:
        if star_first_x > column > star_second_x:
            count += 1

    for row in empty_rows:
        if star_first_y > row > star_second_y:
            count += 1

    return diff + count * (empty_expansion_amount - 1)

def calculate_length_sum(galaxy: list[str], empty_expansion_amount: int):
    empty_rows, empty_columns = get_expanded_indexes(galaxy)
    stars = [Point(x, y) for y, row in enumerate(galaxy) for x, symbol in enumerate(row) if symbol == "#"]

    return sum(get_star_distance3(star1, star2, empty_rows, empty_columns, empty_expansion_amount) for i, star1 in enumerate(stars) for star2 in stars[i+1:])

def silver_solution(lines: list[str]) -> int:
    return calculate_length_sum(lines, 2)

def gold_solution(lines: list[str]) -> int:
    return calculate_length_sum(lines, 1_000_000)
