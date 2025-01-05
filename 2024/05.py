def parse_input(lines: list[str]) -> tuple[list[tuple[int, int]], list[list[int]]]:
    empty_line = lines.index("")
    ordering_rules = [
        (int(left), int(right))
        for line in lines[:empty_line]
        for left, right in [line.split("|")]
    ]
    orders = [[int(x) for x in line.split(",")] for line in lines[empty_line + 1 :]]

    return ordering_rules, orders

def is_order_correct(order: list[int], rules: list[tuple[int, int]]) -> bool:
    for left, right in rules:
        if left not in order or right not in order:
            continue

        if not order.index(left) < order.index(right):
            return False

    return True

def silver_solution(lines: list[str]) -> int:
    ordering_rules, orders = parse_input(lines)

    return sum(
        order[len(order) // 2]
        for order in orders
        if is_order_correct(order, ordering_rules)
    )

def gold_solution(lines: list[str]) -> int:
    ordering_rules, orders = parse_input(lines)

    order_sum = 0

    for order in orders:
        if is_order_correct(order, ordering_rules):
            continue

        while not is_order_correct(order, ordering_rules):
            for left, right in ordering_rules:
                if left not in order or right not in order:
                    continue

                left_index = order.index(left)
                right_index = order.index(right)

                if not left_index < right_index:
                    order[left_index], order[right_index] = order[right_index], order[left_index]

        order_sum += order[len(order) // 2]

    return order_sum
