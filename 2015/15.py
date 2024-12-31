# pylint: disable-all

from utils.string import get_ints



def silver_solution(lines: list[str]) -> int:
    ingredients_list = [get_ints(line, True) for line in lines]

    # Total number to split
    total = 100
    parts = 4

    # Generate all combinations of 4 positive integers that sum to 100
    combinations = []
    for a in range(1, total - parts + 2):
        for b in range(1, total - a - parts + 3):
            for c in range(1, total - a - b - parts + 4):
                d = total - a - b - c
                if d > 0:
                    combinations.append((a, b, c, d))



    maximum = 0
    for combination in combinations: # (1, 1, 1, 96)
        results = [0, 0, 0, 0]

        for i, ingredients in enumerate(ingredients_list): # 0, [2, 0, -2, 0, 3]
            amount = combination[i]

            for f, ingredient in enumerate(ingredients[:-1]): # 2, 0, -2, 0, 3
                results[f] += amount * ingredient

        if any(x < 0 for x in results):
            final_res = 0
        else:
            final_res = results[0] * results[1] * results[2] * results[3]

        maximum = max(maximum, final_res)

    # Display results
    # for combo in combinations:
        # print(combo)

    # print(f"Total combinations: {len(combinations)}")
    # print(combinations)

    return maximum

def gold_solution(lines: list[str]) -> int:
    ingredients_list = [get_ints(line, True) for line in lines]

    # Total number to split
    total = 100
    parts = 4

    # Generate all combinations of 4 positive integers that sum to 100
    combinations = []
    for a in range(1, total - parts + 2):
        for b in range(1, total - a - parts + 3):
            for c in range(1, total - a - b - parts + 4):
                d = total - a - b - c
                if d > 0:
                    combinations.append((a, b, c, d))



    maximum = 0
    for combination in combinations: # (1, 1, 1, 96)
        total_calories = 0
        for i, ingredients in enumerate(ingredients_list): # 0, [2, 0, -2, 0, 3]
            amount = combination[i]
            calories = ingredients[-1]
            total_calories += amount * calories

        if total_calories != 500:
            continue

        results = [0, 0, 0, 0]

        for i, ingredients in enumerate(ingredients_list): # 0, [2, 0, -2, 0, 3]
            amount = combination[i]

            for f, ingredient in enumerate(ingredients[:-1]): # 2, 0, -2, 0, 3
                results[f] += amount * ingredient

        if any(x < 0 for x in results):
            final_res = 0
        else:
            final_res = results[0] * results[1] * results[2] * results[3]

        maximum = max(maximum, final_res)

    # Display results
    # for combo in combinations:
        # print(combo)

    # print(f"Total combinations: {len(combinations)}")
    # print(combinations)

    return maximum