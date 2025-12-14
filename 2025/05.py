from utils.ranges import Range

def parse_input(lines: list[str]) -> tuple[list[Range], list[int]]:
    empty_line = lines.index("")
    ranges = [Range(int(left), int(right)) for left, right in (line.split("-") for line in lines[:empty_line])]
    ingredients = [int(line) for line in lines[empty_line+1:]]

    return ranges, ingredients

def silver_solution(lines: list[str]) -> int:
    ranges, ingredients = parse_input(lines)
    return sum(1 for ingredient in ingredients if any(range.start <= ingredient <= range.end for range in ranges))

def gold_solution(lines: list[str]) -> int:
    ranges, _ = parse_input(lines)
    return sum(range.count() for range in Range.combine_ranges(ranges))
