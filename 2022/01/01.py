
def get_grouped_calories_sum(lines: list[str]) -> list[int]:
    groups: list[int] = []
    current_group: list[int] = []

    for line in lines:
        if not line:
            groups.append(sum(current_group))
            current_group = []
            continue

        current_group.append(int(line))

    if len(current_group) > 0:
        groups.append(sum(current_group))

    return groups

def silver_solution(lines: list[str]) -> int:
    groups = get_grouped_calories_sum(lines)
    return max(groups)

def gold_solution(lines: list[str]) -> int:
    groups = get_grouped_calories_sum(lines)
    return sum(sorted(groups, reverse=True)[:3])
