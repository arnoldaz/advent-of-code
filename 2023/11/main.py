
file_name = "input.txt"
with open(file_name) as file:
    lines = [line.rstrip() for line in file]

def get_expanded_indexes(lines: list[str]) -> tuple[list[int], list[int]]:
    empty_rows: list[int] = [] 
    empty_columns: list[int] = [] 

    for i, line in enumerate(lines):
        if all(char == "." for char in line):
            empty_rows.append(i)

    for i in range(len(lines[0])):
        if all(char == "." for char in [line[i] for line in lines]):
            empty_columns.append(i)

    return (empty_rows, empty_columns)

def get_expanded_galaxy(lines: list[str]) -> list[str]:
    empty_rows, empty_columns = get_expanded_indexes(lines)
    new_lines = lines[:]

    insertion_index = 0
    for i in range(len(new_lines[0]) + len(empty_columns)):
        if i - insertion_index in empty_columns:
            for line_index in range(len(new_lines)):
                new_lines[line_index] = new_lines[line_index][:i] + "." + new_lines[line_index][i:]
            empty_columns.remove(i - insertion_index)
            insertion_index += 1

    insertion_index = 0
    for i in range(len(new_lines) + len(empty_rows)):
        if i - insertion_index in empty_rows:
            new_lines.insert(i, "." * len(new_lines[0]))
            empty_rows.remove(i - insertion_index)
            insertion_index += 1
            
    return new_lines

def get_star_distance(star1: tuple[int, int], star2: tuple[int, int]) -> int:
    x_diff = star1[0] - star2[0] if star1[0] >= star2[0] else star2[0] - star1[0]
    y_diff = star1[1] - star2[1] if star1[1] >= star2[1] else star2[1] - star1[1]

    return x_diff + y_diff

def calculate_length_sum(galaxy: list[str]) -> int:
    stars: list[tuple[int, int]] = []

    for y in range(len(galaxy)):
        for x in range(len(galaxy[0])):
            if galaxy[y][x] == "#":
                stars.append((x, y))

    sum = 0
    for i in range(len(stars)):
        for j in range(i + 1, len(stars)):
            distance = get_star_distance(stars[i], stars[j])
            sum += distance

    return sum

def get_star_distance_million(star1: tuple[int, int], star2: tuple[int, int], empty_rows: list[int], empty_columns: list[int]) -> int:
    star_first_x = star1[0] if star1[0] >= star2[0] else star2[0]
    star_second_x = star2[0] if star1[0] >= star2[0] else star1[0]

    x_diff = star_first_x - star_second_x
    for column in empty_columns:
        if star_first_x > column > star_second_x:
            x_diff += 1_000_000 - 1

    star_first_y = star1[1] if star1[1] >= star2[1] else star2[1]
    star_second_y = star2[1] if star1[1] >= star2[1] else star1[1]

    y_diff = star_first_y - star_second_y
    for row in empty_rows:
        if star_first_y > row > star_second_y:
            y_diff += 1_000_000 - 1

    return x_diff + y_diff

def calculate_length_sum_million(galaxy: list[str]):
    empty_rows, empty_columns = get_expanded_indexes(galaxy)   
    stars: list[tuple[int, int]] = []

    for y in range(len(galaxy)):
        for x in range(len(galaxy[0])):
            if galaxy[y][x] == "#":
                stars.append((x, y))

    sum = 0
    for i in range(len(stars)):
        for j in range(i + 1, len(stars)):
            distance = get_star_distance_million(stars[i], stars[j], empty_rows, empty_columns)
            sum += distance

    return sum

print(f"{calculate_length_sum(get_expanded_galaxy(lines))=}")
print(f"{calculate_length_sum_million(lines)=}")