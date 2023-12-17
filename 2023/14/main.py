
with open("input.txt") as file:
    lines = [line.rstrip() for line in file]

def slide_north(lines: list[str]) -> tuple[list[str], bool]:
    new_lines = lines[:]
    
    changed = False
    for i in range(1, len(new_lines)):
        for j in range(0, len(new_lines[i])):
            if new_lines[i][j] == "O" and new_lines[i-1][j] == ".":
                new_lines[i] = new_lines[i][:j] + "." + new_lines[i][j+1:]
                new_lines[i-1] = new_lines[i-1][:j] + "O" + new_lines[i-1][j+1:]
                changed = True
                
    return new_lines, changed

def calculate_points(final_lines: list[str]) -> int:
    line_count = len(final_lines)
    answer = 0

    for i, line in enumerate(final_lines):
        count = line.count("O")
        answer += (line_count - i) * count

    return answer

def get_single_slide_north_points(lines: list[str]) -> int:
    changed = True
    new_lines = lines[:]
    while changed:
        new_lines, changed = slide_north(new_lines)

    return calculate_points(new_lines)

def rotate_matrix(lines):
    return ["".join(line) for line in zip(*lines[::-1])]

lines_cache: dict[str, tuple[list[str], int]] = {}

def slide_cycle(lines: list[str], iteration: int) -> tuple[list[str], int]:
    hashmap_key = "".join(lines)
    if hashmap_key in lines_cache:
        return lines_cache[hashmap_key]

    new_lines = lines[:]
    changed = True
    
    # north
    while changed:
        new_lines, changed = slide_north(new_lines)
        
    # west
    changed = True
    new_lines = rotate_matrix(new_lines)
    while changed:
        new_lines, changed = slide_north(new_lines)

    # sount
    changed = True
    new_lines = rotate_matrix(new_lines)
    while changed:
        new_lines, changed = slide_north(new_lines)

    # east
    changed = True
    new_lines = rotate_matrix(new_lines)
    while changed:
        new_lines, changed = slide_north(new_lines)

    # rotate back to north
    new_lines = rotate_matrix(new_lines)

    lines_cache[hashmap_key] = (new_lines, iteration)

    return new_lines, iteration

ITERATION_COUNT = 1_000_000_000

def calculate_actual_iteration_periodic(lines: list[str]) -> int:
    initial_iterations = 0
    initial_iterations_over = False

    repeated_start_recorded = False
    repeated_first_value = -1
    repeated_first_index = -1
    repeated_rotation_length = -1

    new_lines = lines[:]
    for i in range(ITERATION_COUNT):
        new_lines, iter = slide_cycle(new_lines, i)

        if i == iter and not initial_iterations_over:
            initial_iterations += 1
        else:
            initial_iterations_over = True

        if initial_iterations_over and not repeated_start_recorded:
            repeated_first_value = iter
            repeated_first_index = i
            repeated_start_recorded = True
        elif repeated_start_recorded and repeated_first_value == iter:
            repeated_rotation_length = i - repeated_first_index
            break

    return ((ITERATION_COUNT - initial_iterations) % repeated_rotation_length) + initial_iterations

def calculate_all_cycle_load(lines: list[str]) -> int:
    actual_iterations = calculate_actual_iteration_periodic(lines)

    new_lines = lines[:]
    for i in range(actual_iterations):
        new_lines, _ = slide_cycle(new_lines, i)

    return calculate_points(new_lines)

print(f"{get_single_slide_north_points(lines)=}")
print(f"{calculate_all_cycle_load(lines)=}") # takes ~10s

