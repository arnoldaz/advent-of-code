def parse_input(lines: list[str]) -> list[tuple[int, int, int]]:
    return [tuple[int, int, int](map(int, line.split("x"))) for line in lines]

def silver_solution(lines: list[str]) -> int:
    all_dimensions = parse_input(lines)

    total_area = 0
    for l, w, h in all_dimensions:
        total_area += 2*l*w + 2*w*h + 2*h*l
        x, y = sorted((l, w, h))[:2]
        total_area += x * y

    return total_area

def gold_solution(lines: list[str]) -> int:
    all_dimensions = parse_input(lines)

    total_length = 0
    for l, w, h in all_dimensions:
        x, y = sorted((l, w, h))[:2]
        total_length += 2*x + 2*y
        total_length += l*w*h

    return total_length
