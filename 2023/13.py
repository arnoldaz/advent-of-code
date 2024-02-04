from typing import Optional
from utils.matrix import Matrix
from utils.string import nearly_equal

def parse_input(lines: list[str]) -> list[Matrix[str]]:
    patterns: list[Matrix[str]] = []
    current_pattern_data: list[str] = []

    for line in lines:
        if line.strip():
            current_pattern_data.append(line)
            continue

        patterns.append(Matrix[str](current_pattern_data, str))
        current_pattern_data = []

    patterns.append(Matrix[str](current_pattern_data, str))
    return patterns

def get_horizontal_reflection_line(pattern: Matrix[str], require_single_change: bool) -> Optional[int]:
    line_length = pattern.height()
    diff_amount = 0

    for i in range(0, line_length - 1):
        # If 2 nearby lines are equal, it is a possible reflection center
        if pattern.get_row(i) != pattern.get_row(i + 1):
            continue

        # Check line equality going both ways from the possible reflection center
        j = 1
        while True:
            if i - j < 0 or i + j + 1 > line_length - 1:
                # If change is required and no changes happened, reflection center is invalid
                if not require_single_change or diff_amount > 0:
                    return i + 1
                break

            # Check single change but allow passing only once
            if require_single_change and diff_amount == 0 and nearly_equal(pattern.get_row(i - j), pattern.get_row(i + j + 1)):
                diff_amount += 1
                j += 1
                continue

            if pattern.get_row(i - j) != pattern.get_row(i + j + 1):
                break

            j += 1

    if not require_single_change:
        return None

    # Previous loop relies on finding 2 equal nearby lines but doesn't account having required change on those center lines
    # Need to loop again checking only for difference in those 2 center lines
    diff_amount = 0
    for i in range(0, line_length - 1):
        if nearly_equal(pattern.get_row(i), pattern.get_row(i + 1)):
            j = 1
            while True:
                if i - j < 0 or i + j + 1 > line_length - 1:
                    return i + 1

                if pattern.get_row(i - j) != pattern.get_row(i + j + 1):
                    break

                j += 1

    return None

def get_vertical_reflection_line(pattern: Matrix[str], allow_single_change: bool) -> Optional[int]:
    pattern.rotate_clockwise()
    return get_horizontal_reflection_line(pattern, allow_single_change)

def get_patterns_sum(patterns: list[Matrix[str]], allow_single_change: bool) -> int:
    final_sum = 0
    for pattern in patterns:
        horizontal = get_horizontal_reflection_line(pattern, allow_single_change)
        if horizontal is not None:
            final_sum += horizontal * 100
            continue

        vertical = get_vertical_reflection_line(pattern, allow_single_change)
        if vertical is not None:
            final_sum += vertical

    return final_sum

def silver_solution(lines: list[str]) -> int:
    patterns = parse_input(lines)
    return get_patterns_sum(patterns, False)

def gold_solution(lines: list[str]) -> int:
    patterns = parse_input(lines)
    return get_patterns_sum(patterns, True)
