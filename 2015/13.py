from itertools import permutations

def parse_input(lines: list[str]) -> dict[str, dict[str, int]]:
    happiness_map: dict[str, dict[str, int]] = {}
    for line in lines:
        words = line.split()
        name1, change, amount, name2 = words[0], words[2], int(words[3]), words[10].removesuffix(".")
        amount = amount if change == "gain" else -amount
        happiness_map.setdefault(name1, {})[name2] = amount

    return happiness_map

def calculate_total_happiness(permutation: tuple[str, ...], happiness_map: dict[str, dict[str, int]]):
    total_happiness = 0
    for i, name in enumerate(permutation):
        left = permutation[i-1]
        right = permutation[i+1] if i != len(permutation) - 1 else permutation[0]
        name_happiness_map = happiness_map[name]
        total_happiness += name_happiness_map[left] + name_happiness_map[right]

    return total_happiness

def silver_solution(lines: list[str]) -> int:
    happiness_map = parse_input(lines)
    names = happiness_map.keys()

    return max(
        calculate_total_happiness(permutation, happiness_map)
        for permutation in permutations(names)
    )

def gold_solution(lines: list[str]) -> int:
    happiness_map = parse_input(lines)
    for name in list(happiness_map.keys()):
        happiness_map.setdefault("me", {})[name] = 0
        happiness_map[name]["me"] = 0
    names = happiness_map.keys()

    return max(
        calculate_total_happiness(permutation, happiness_map)
        for permutation in permutations(names)
    )
