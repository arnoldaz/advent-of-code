import math
from typing import NamedTuple

class Monkey(NamedTuple):
    index: int
    items: list[int]
    operation: tuple[str, str, str]
    divisible_test: int
    if_divisible_true: int
    if_divisible_false: int

def parse_input(lines: list[str]) -> list[Monkey]:
    monkeys: list[Monkey] = []

    i = 0
    while i < len(lines):
        index = int(lines[i].removeprefix("Monkey ").removesuffix(":"))
        items = [int(item) for item in lines[i+1].removeprefix("  Starting items: ").split(", ")]
        operation = tuple[str, str, str](lines[i+2].removeprefix("  Operation: new = ").split())
        divisible_test = int(lines[i+3].removeprefix("  Test: divisible by "))
        if_divisible_true = int(lines[i+4].removeprefix("    If true: throw to monkey "))
        if_divisible_false = int(lines[i+5].removeprefix("    If false: throw to monkey "))

        monkeys.append(Monkey(index, items, operation, divisible_test, if_divisible_true, if_divisible_false))
        i += 7

    return monkeys

def calculate_operation_result(old_number: int, operation: tuple[str, str, str]) -> int:
    operand_left, operator, operand_right = operation

    left = old_number if operand_left == "old" else int(operand_left)
    right = old_number if operand_right == "old" else int(operand_right)

    match operator:
        case "+":
            return left + right
        case "*":
            return left * right
        case _:
            raise ValueError(f"Unknown operator found: '{operator}'")

def silver_solution(lines: list[str]) -> int:
    monkeys = parse_input(lines)
    inspection_count = [0 for _ in monkeys]

    for _ in range(20):
        for i, monkey in enumerate(monkeys):
            for item in monkey.items[:]:
                worry_level = calculate_operation_result(item, monkey.operation)
                worry_level //= 3

                next_monkey = monkey.if_divisible_true if worry_level % monkey.divisible_test == 0 else monkey.if_divisible_false
                monkey.items.pop(monkey.items.index(item))
                monkeys[next_monkey].items.append(worry_level)

                inspection_count[i] += 1

    inspection_count.sort(reverse=True)
    return inspection_count[0] * inspection_count[1]

def gold_solution(lines: list[str]) -> int:
    monkeys = parse_input(lines)
    inspection_count = [0 for _ in monkeys]
    common_multiple = math.prod(monkey.divisible_test for monkey in monkeys)

    for _ in range(10_000):
        for i, monkey in enumerate(monkeys):
            for item in monkey.items[:]:
                worry_level = calculate_operation_result(item, monkey.operation)
                worry_level %= common_multiple

                next_monkey = monkey.if_divisible_true if worry_level % monkey.divisible_test == 0 else monkey.if_divisible_false
                monkey.items.pop(monkey.items.index(item))
                monkeys[next_monkey].items.append(worry_level)

                inspection_count[i] += 1

    inspection_count.sort(reverse=True)
    return inspection_count[0] * inspection_count[1]
