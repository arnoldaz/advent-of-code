from functools import cache

def parse_input(lines: list[str]) -> tuple[list[str], list[str]]:
    patterns = lines[0].split(", ")
    return patterns, lines[2:]

def find_arrangement_count(patterns: list[str], target_design: str):
    @cache
    def find_arrangement_count_recursive(current_design: str) -> int:
        if current_design == target_design:
            return 1

        return sum(
            find_arrangement_count_recursive(current_design + pattern)
            for pattern in patterns
            if target_design.startswith(current_design + pattern))

    return find_arrangement_count_recursive("")

def silver_solution(lines: list[str]) -> int:
    patterns, designs = parse_input(lines)
    return sum(1 for design in designs if find_arrangement_count(patterns, design) > 0)

def gold_solution(lines: list[str]) -> int:
    patterns, designs = parse_input(lines)
    return sum(find_arrangement_count(patterns, design) for design in designs)
