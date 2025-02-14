def parse_input(lines: list[str]) -> list[tuple[int, int, int]]:
    return [tuple[int, int, int](int(x) for x in line.split()) for line in lines]

def calculate_valid_triangle_count(triples: list[tuple[int, int, int]]) -> int:
    return sum(1 for x, y, z in triples if x + y + z > 2 * max(x, y, z))

def silver_solution(lines: list[str]) -> int:
    triples = parse_input(lines)

    return calculate_valid_triangle_count(triples)

def gold_solution(lines: list[str]) -> int:
    triples = parse_input(lines)
    trios_of_triples = [triples[i:i+3] for i in range(0, len(triples), 3)]
    transposed_trios = [list(zip(*reversed(x))) for x in trios_of_triples]
    flattened_triples = [item for sublist in transposed_trios for item in sublist]

    return calculate_valid_triangle_count(flattened_triples)
