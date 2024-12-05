def is_order_correct(order: list[int], rules: list[tuple[int, int]]) -> bool:
    for rule in rules:
        if rule[0] not in order or rule[1] not in order:
            continue

        if not order.index(rule[0]) < order.index(rule[1]):
            return False
            
    return True
 
def parse_input(lines: list[str]) -> tuple[list[tuple[int, int]], list[list[int]]]:
    ordering_rules: list[tuple[int, int]] = []
    orders: list[list[int]] = []

    is_reading_rules = True
    for line in lines:
        if is_reading_rules:
            if not line:
                is_reading_rules = False
                continue

            rule_left, rule_right = line.split("|")
            ordering_rules.append((int(rule_left), int(rule_right)))
        else:
            order = [int(x) for x in line.split(",")]
            orders.append(order)

    return ordering_rules, orders

def silver_solution(lines: list[str]) -> int:
    ordering_rules, orders = parse_input(lines)

    order_sum = 0

    for order in orders:
        if is_order_correct(order, ordering_rules):
            order_sum += order[len(order) // 2]

    return order_sum

def gold_solution(lines: list[str]) -> int:
    ordering_rules, orders = parse_input(lines)

    order_sum = 0

    for order in orders:
        if is_order_correct(order, ordering_rules):
            continue

        while not is_order_correct(order, ordering_rules):
            for rule in ordering_rules:
                if rule[0] not in order or rule[1] not in order:
                    continue

                index1 = order.index(rule[0])
                index2 = order.index(rule[1])

                if not index1 < index2:
                     order[index1], order[index2] = order[index2], order[index1]

        order_sum += order[len(order) // 2]

    return order_sum
