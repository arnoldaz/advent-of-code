# pylint: disable-all
from itertools import combinations, product
from typing import NamedTuple
import sympy

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
    machines = parse_input(lines)
    answer = 0

    xxx = 0
    for machine in machines:
        print(xxx, len(machines))
        xxx+=1
        n = len(machine.buttons)
        x = sympy.symbols(f"x0:{n}")
        equations = []

        for i in range(len(machine.joltage_requirements)):
            required_variables = []
            for button_index, button in enumerate(machine.buttons):
                if i in button:
                    required_variables.append(button_index)

            # print(i, required_variables, machine.joltage_requirements[i])
            equations.append(sympy.Eq(sum(x[index] for index in required_variables), machine.joltage_requirements[i]))

        # print(equations)
        solutions = sympy.linsolve(equations, x)
        # print(solutions)
        
        parametric_solution = list(solutions)[0] # type: ignore
        free_symbols = list(parametric_solution.free_symbols)
        max_value = max(machine.joltage_requirements)

        concrete_solutions = []
        for values in product(range(max_value + 1), repeat=len(free_symbols)):
            subs_dict = dict(zip(free_symbols, values))
            concrete_solution = [s.subs(subs_dict) for s in parametric_solution]
            if all(value >= 0 for value in concrete_solution):
                concrete_solutions.append(tuple(int(v) for v in concrete_solution))

        min_presses = min(sum(s) for s in concrete_solutions)
        answer += min_presses

    return answer
