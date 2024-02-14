from enum import Enum
from typing import NamedTuple

class ModuleType(Enum):
    NORMAL = 1
    FLIP_FLOP = 2
    CONJUNCTION = 3

class Module(NamedTuple):
    variable: str
    type: ModuleType
    destinations: list[str]

def parse_input(lines: list[str]) -> dict[str, Module]:
    modules: dict[str, Module] = {}

    for line in lines:
        source, destination = line.split(" -> ")

        if source.startswith("%"):
            module_type = ModuleType.FLIP_FLOP
            variable = source.removeprefix("%")
        elif source.startswith("&"):
            module_type = ModuleType.CONJUNCTION
            variable = source.removeprefix("&")
        else:
            module_type = ModuleType.NORMAL
            variable = source

        destinations = destination.split(", ")
        modules[variable] = Module(variable, module_type, destinations)

    return modules

def calculate_pulses_recursive(modules_and_pulses: list[tuple[Module, bool]], modules: dict[str, Module], flip_flop_states: dict[str, bool], conjunction_states: dict[str, list[tuple[str, bool]]]) -> tuple[int, int]:
    low_pulse_count, high_pulse_count = 0, 0
    next_modules: list[tuple[Module, bool]] = []
    for module_and_pulse in modules_and_pulses:
        module, pulse = module_and_pulse
        for module_name in module.destinations:
            if pulse:
                high_pulse_count += 1
            else:
                low_pulse_count += 1

            if module_name not in modules:
                # print(f"{module.variable} -{"high" if pulse else "low"}-> {module_name}")
                continue

            new_module = modules[module_name]
            # print(f"{module.variable} -{"high" if pulse else "low"}-> {new_module.variable}")
            match new_module.type:
                case ModuleType.NORMAL:
                    new_pulse = pulse
                case ModuleType.FLIP_FLOP:
                    if not pulse:
                        old_state = flip_flop_states[new_module.variable]
                        new_state = not old_state
                        flip_flop_states[new_module.variable] = new_state

                        new_pulse = not old_state
                    else:
                        continue
                case ModuleType.CONJUNCTION:
                    state_list = conjunction_states[new_module.variable]
                    for i, (state_name, _) in enumerate(state_list):
                        if state_name == module.variable:
                            state_list[i] = (state_name, pulse)

                    if all(state_pulse for (_, state_pulse) in state_list):
                        new_pulse = False
                    else:
                        new_pulse = True

            next_modules.append((new_module, new_pulse))

    if len(next_modules) > 0:
        child_low_pulse_count, child_high_pulse_count = calculate_pulses_recursive(next_modules, modules, flip_flop_states, conjunction_states)
        low_pulse_count += child_low_pulse_count
        high_pulse_count += child_high_pulse_count

    return low_pulse_count, high_pulse_count

def calculate_pulses(modules: dict[str, Module]):
    flip_flop_states: dict[str, bool] = { value.variable: False for value in modules.values() if value.type == ModuleType.FLIP_FLOP }
    conjunction_states: dict[str, list[tuple[str, bool]]] = { value.variable: [(input, False) for input in modules if value.variable in modules[input].destinations] for value in modules.values() if value.type == ModuleType.CONJUNCTION }

    start_module = modules["broadcaster"]
    start_pulse = False

    total_low_pulse_count, total_high_pulse_count = 0, 0

    for _ in range(1_000):
        total_low_pulse_count += 1
        # print(f"button -{"high" if start_pulse else "low"}-> {start_module.variable}")

        low_pulse_count, high_pulse_count = calculate_pulses_recursive([(start_module, start_pulse)], modules, flip_flop_states, conjunction_states)
        total_low_pulse_count += low_pulse_count
        total_high_pulse_count += high_pulse_count

    return total_low_pulse_count * total_high_pulse_count

def silver_solution(lines: list[str]) -> int:
    modules = parse_input(lines)
    return calculate_pulses(modules)

def gold_solution(_lines: list[str]) -> int:
    # Implement solution
    return -321
