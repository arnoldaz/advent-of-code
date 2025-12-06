from utils.list import remove_list_indexes
from utils.ranges import Range

def parse_input(lines: list[str]) -> tuple[list[tuple[int, int]], list[int]]:
    empty_line = lines.index("")
    ranges: list[tuple[int, int]] = []

    for line in lines[:empty_line]:
        left, right = line.split("-")
        ranges.append((int(left), int(right)))

    ingredients = [int(line) for line in lines[empty_line+1:]]

    return ranges, ingredients

def silver_solution(lines: list[str]) -> int:
    ranges, ingredients = parse_input(lines)
    answer = 0

    for ingredient in ingredients:
        for left, right in ranges:
            if ingredient >= left and ingredient <= right:
                answer += 1
                break

    return answer

def gold_solution(lines: list[str]) -> int:
    old_ranges, _ = parse_input(lines)
    answer = 0

    ranges = [Range(left, right) for left, right in old_ranges]
    parsed_ranges: list[Range] = []

    for number_range in ranges:
        answer += number_range.count()

        remove_parsed_range_indices: list[int] = []
        add_ranges: list[Range] = []
        for i, parsed_range in enumerate(parsed_ranges):
            if (overlap := number_range.find_overlap(parsed_range)) is not None:
                answer -= overlap.count()
                remove_parsed_range_indices.append(i)
                add_ranges.append(number_range)
                add_ranges += parsed_range.remove_overlapping_range(overlap)

        # print(f"{range=}, {parsed_ranges=}, {remove_parsed_range_indices=}, {add_ranges=}")
        remove_list_indexes(parsed_ranges, remove_parsed_range_indices)
        if len(add_ranges) == 0:
            parsed_ranges.append(number_range)
        else:
            parsed_ranges += add_ranges

        parsed_ranges = list(set(parsed_ranges))

    return answer
