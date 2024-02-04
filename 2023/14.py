from utils.matrix import Matrix

def slide_north_once(platform: Matrix[str]) -> bool:
    data = platform.get_data()
    height, width = platform.height(), platform.width()

    anything_changed = False
    for y in range(1, height):
        for x in range(0, width):
            if data[y][x] == "O" and data[y-1][x] == ".":
                data[y][x] = "."
                data[y-1][x] = "O"
                anything_changed = True

    return anything_changed

def slide_north(platform: Matrix[str]):
    while slide_north_once(platform):
        pass

def slide_cycle_matrix(platform: Matrix[str]):
    # north
    slide_north(platform)

    # west
    platform.rotate_clockwise()
    slide_north(platform)

    # south
    platform.rotate_clockwise()
    slide_north(platform)

    # east
    platform.rotate_clockwise()
    slide_north(platform)

    # rotate back to north
    platform.rotate_clockwise()

def calculate_platform_points(platform: Matrix[str]) -> int:
    line_count = platform.height()
    return sum((line_count - y) * line.count("O") for y, line in enumerate(platform.get_data()))

def perform_cycles(platform: Matrix[str], total_iterations: int):
    initial_iterations = 0
    initial_iterations_over = False

    repeated_start_recorded = False
    repeated_first_value = -1
    repeated_first_index = -1
    repeated_rotation_length = -1

    matrix_cache: dict[str, int] = {}

    for i in range(total_iterations):
        slide_cycle_matrix(platform)

        cache_key = "|".join(["".join(row) for row in platform.get_data()])

        if cache_key in matrix_cache:
            iteration = matrix_cache.get(cache_key)
        else:
            iteration = i
            matrix_cache[cache_key] = i

        if i == iteration and not initial_iterations_over:
            initial_iterations += 1
        else:
            initial_iterations_over = True

        if initial_iterations_over and not repeated_start_recorded:
            repeated_first_value = iteration
            repeated_first_index = i
            repeated_start_recorded = True
        elif repeated_start_recorded and repeated_first_value == iteration:
            repeated_rotation_length = i - repeated_first_index
            break

    required_iteration = ((total_iterations - initial_iterations) % repeated_rotation_length) + initial_iterations - (repeated_rotation_length + 1)
    required_cached_data = list(matrix_cache.keys())[list(matrix_cache.values()).index(required_iteration)].split("|")
    platform.initialize(required_cached_data, str)

def silver_solution(lines: list[str]) -> int:
    platform = Matrix[str](lines, str)
    slide_north(platform)

    return calculate_platform_points(platform)

def gold_solution(lines: list[str]) -> int:
    platform = Matrix[str](lines, str)
    perform_cycles(platform, 1_000_000_000)

    return calculate_platform_points(platform)
