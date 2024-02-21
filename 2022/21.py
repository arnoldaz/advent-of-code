# pylint: disable=unused-argument



def parse_input(lines: list[str]) -> dict[str, int | tuple[str, str, str]]:
    monkeys: dict[str, int | tuple[str, str, str]] = {}
    for line in lines:
        name, other = line.split(": ")
        if other.isnumeric():
            monkeys[name] = int(other)
        else:
            monkeys[name] = tuple[str, str, str](other.split())

    return monkeys

def get_monkey_number(monkeys: dict[str, int | tuple[str, str, str]], monkey_name: str) -> int:
    output = monkeys[monkey_name]
    if isinstance(output, int):
        return output

    first_name, operator, second_name = output
    first_number = get_monkey_number(monkeys, first_name)
    second_number = get_monkey_number(monkeys, second_name)

    match operator:
        case "+":
            return first_number + second_number
        case "-":
            return first_number - second_number
        case "*":
            return first_number * second_number
        case "/":
            return first_number // second_number
        case _:
            raise ValueError(f"Unknown operator '{operator}'")

def get_monkey_path(monkeys: dict[str, int | tuple[str, str, str]], start_monkey: str, end_monkey: str, path: list[str]) -> bool:
    path.append(start_monkey)

    if start_monkey == end_monkey:
        return True

    output = monkeys[start_monkey]
    if isinstance(output, int):
        path.pop()
        return False

    first_name, _, second_name = output

    if get_monkey_path(monkeys, first_name, end_monkey, path):
        return True

    if get_monkey_path(monkeys, second_name, end_monkey, path):
        return True

    path.pop()
    return False

def find_equality_test_value(monkeys: dict[str, int | tuple[str, str, str]], start_monkey: str, test_monkey: str, path: list[str]):
    output = monkeys[start_monkey]
    assert not isinstance(output, int)

    first_name, _, second_name = output
    end_branch = path[1] # "pppw"
    non_end_branch = second_name if first_name == end_branch else first_name # "sjwn"
    non_end_value_previous = get_monkey_number(monkeys, non_end_branch) # 150

    for segment in path[2:]:
        output = monkeys[end_branch] # cczh / lfqf
        assert not isinstance(output, int)
        first_name, operator, second_name = output
        end_branch = segment # cczh
        non_end_branch, is_unknown_first = (second_name, True) if first_name == end_branch else (first_name, False) # lfqf
        non_end_value = get_monkey_number(monkeys, non_end_branch) # 4

        print(f"{end_branch=} {non_end_branch=} {non_end_value=} {non_end_value_previous=} {operator=} {is_unknown_first=} ", end="")
        match operator:
            case "+":
                non_end_value_previous -= non_end_value
            case "-":
                if is_unknown_first: # x - 3 = 5
                    non_end_value_previous = non_end_value_previous + non_end_value
                else: # 3 - x = 5
                    non_end_value_previous = non_end_value - non_end_value_previous
            case "*":
                non_end_value_previous /= non_end_value
            case "/":
                if is_unknown_first:
                    non_end_value_previous = non_end_value_previous * non_end_value # 600
                else:
                    non_end_value_previous = non_end_value / non_end_value_previous
            case _:
                raise ValueError(f"Unknown operator '{operator}'")
        print(f"after {non_end_value_previous=}")

    return non_end_value_previous

def silver_solution(lines: list[str]) -> int:
    monkeys = parse_input(lines)
    return get_monkey_number(monkeys, "root")

def gold_solution(lines: list[str]):
    monkeys = parse_input(lines)

    path = []
    get_monkey_path(monkeys, "root", "humn", path)
    # print(path)

    return find_equality_test_value(monkeys, "root", "humn", path)
