from enum import Enum
from typing import NamedTuple

with open("input.txt") as file:
    lines = [line.rstrip() for line in file]

class ModuleType(Enum):
    Normal = 1
    FlipFlop = 2
    Conjunction = 3

class Module(NamedTuple):
    variable: str
    type: ModuleType
    destinations: list[str]

modules: dict[str, Module] = {}

for line in lines:
    source, destination = line.split(" -> ")
    
    if source.startswith("%"):
        type = ModuleType.FlipFlop
        variable = source.removeprefix("%")
    elif source.startswith("&"):
        type = ModuleType.Conjunction
        variable = source.removeprefix("&")
    else:
        type = ModuleType.Normal
        variable = source
        
    destinations = destination.split(", ")
    
    modules[variable] = Module(variable, type, destinations)

high_pulse_count = 0
low_pulse_count = 0
def calculate_pulses_recursive(modules_and_pulses: list[tuple[Module, bool]], map: dict[str, Module], flip_flop_states: dict[str, bool], conjunction_states: dict[str, list[tuple[str, bool]]], button_counter: int):
    global high_pulse_count
    global low_pulse_count

    next_modules = []

    for module_and_pulse in modules_and_pulses:
        module, pulse = module_and_pulse
        for module_name in module.destinations:
            if pulse:
                high_pulse_count += 1
            else:
                low_pulse_count += 1
        
            if not module_name in map:
                # print(f"{module.variable} -{"high" if pulse else "low"}-> {module_name}")
                continue
            
            new_module = map[module_name]
            match new_module.type:
                case ModuleType.Normal:
                    # print(f"{module.variable} -{"high" if pulse else "low"}-> {new_module.variable}")
                    new_pulse = pulse
                case ModuleType.FlipFlop:
                    if not pulse:
                        old_state = flip_flop_states[new_module.variable]
                        new_state = not old_state
                        flip_flop_states[new_module.variable] = new_state

                        # print(f"{module.variable} -{"high" if pulse else "low"}-> {new_module.variable}")

                        if old_state:
                            new_pulse = False
                        else:
                            new_pulse = True
                    else:
                        # print(f"{module.variable} -{"high" if pulse else "low"}-> {new_module.variable}")
                        continue
                case ModuleType.Conjunction:
                    state_list = conjunction_states[new_module.variable]
                    for i, state in enumerate(state_list):
                        if state[0] == module.variable:
                            state_list[i] = (state[0], pulse)
                    
                    # print(f"{module.variable} -{"high" if pulse else "low"}-> {new_module.variable}")

                    if all(state[1] for state in state_list):
                        new_pulse = False
                    else:
                        new_pulse = True
        

            next_modules.append((new_module, new_pulse))

    if len(next_modules) != 0:
        calculate_pulses_recursive(next_modules, map, flip_flop_states, conjunction_states, button_counter)

def calculate_pulses(modules: dict[str, Module]):
    flip_flop_states: dict[str, bool] = { value.variable: False for value in modules.values() if value.type == ModuleType.FlipFlop }
    conjunction_states: dict[str, list[tuple[str, bool]]] = { value.variable: [(input, False) for input in modules if value.variable in modules[input].destinations] for value in modules.values() if value.type == ModuleType.Conjunction }
    
    start_module = modules["broadcaster"]
    start_pulse = False
    
    global high_pulse_count
    global low_pulse_count

    for i in range(1_000):
        low_pulse_count += 1
        # print(f"button -{"high" if start_pulse else "low"}-> {start_module.variable}")
        calculate_pulses_recursive([(start_module, start_pulse)], modules, flip_flop_states, conjunction_states, i)
    
    print(high_pulse_count)
    print(low_pulse_count)

    return high_pulse_count * low_pulse_count

print(f"{calculate_pulses(modules)=}")