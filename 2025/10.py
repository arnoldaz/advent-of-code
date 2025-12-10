from itertools import combinations
from typing import NamedTuple
from z3 import Int, Optimize, sat, IntNumRef

class Machine(NamedTuple):
    lights: list[bool]
    buttons: list[list[int]]
    joltages: list[int]

def parse_input(lines: list[str]) -> list[Machine]:
    machines: list[Machine] = []
    for line in lines:
        first, *all_middle, last = line.split()
        lights = [symbol == "." for symbol in first.removeprefix("[").removesuffix("]")]
        buttons = [list(map(int, middle.removeprefix("(").removesuffix(")").split(","))) for middle in all_middle]
        joltages = list(map(int, last.removeprefix("{").removesuffix("}").split(",")))

        machines.append(Machine(lights, buttons, joltages))

    return machines

def silver_solution(lines: list[str]) -> int:
    machines = parse_input(lines)
    answer = 0

    for machine in machines:
        button_press_list: list[list[list[int]]] = []
        for length in range(len(machine.buttons) + 1):
            for combination in combinations(machine.buttons, length):
                current_lights = machine.lights[:]
                for button in combination:
                    for element in button:
                        current_lights[element] = not current_lights[element]

                if all(current_lights):
                    button_press_list.append(list(combination))

        answer += len(min(button_press_list, key=len))

    return answer

def gold_solution(lines: list[str]) -> int:
    machines = parse_input(lines)
    answer = 0

    for machine in machines:
        variable_names = [f"x{i}" for i in range(len(machine.buttons))]
        variables = [Int(name) for name in variable_names]

        z3 = Optimize()

        # All variables must be positive integers
        for value in variables:
            z3.add(value >= 0)

        # All joltage sums must be correct
        for i, joltage in enumerate(machine.joltages):
            required_variables = [button_index for button_index, button in enumerate(machine.buttons) if i in button]
            z3.add(sum(variables[index] for index in required_variables) == joltage)

        # Variable sum should be minimal
        z3.minimize(sum(variables))

        if z3.check() != sat:
            return -1

        model = z3.model()
        for variable in variables:
            value = model.eval(variable, model_completion=True)
            assert isinstance(value, IntNumRef)
            answer += value.as_long()

    return answer
