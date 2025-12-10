# pylint: disable-all

from itertools import combinations
from typing import NamedTuple

class Machine(NamedTuple):
    lights: list[bool]
    buttons: list[list[int]]
    joltage_requirements: list[int]

def parse_input(lines: list[str]) -> list[Machine]:
    machines: list[Machine] = []
    for line in lines:
        first, *all_middle, last = line.split()
        lights = [symbol == "." for symbol in first.removeprefix("[").removesuffix("]")]
        buttons = [list(map(int, middle.removeprefix("(").removesuffix(")").split(","))) for middle in all_middle]
        joltage_requirements = list(map(int, last.removeprefix("{").removesuffix("}").split(",")))

        machines.append(Machine(lights, buttons, joltage_requirements))

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

        answer += len(min(button_press_list, key=lambda x: len(x)))

    return answer

def gold_solution(lines: list[str]) -> int:
    # Implement solution
    return -321
