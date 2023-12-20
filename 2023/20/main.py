from enum import Enum
from typing import NamedTuple

with open("input-test2.txt") as file:
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

# for key in modules:
#     print(key, modules[key])

def calculate_pulses_recursive(module: Module, pulse: bool, map: dict[str, Module], flip_flop_states: dict[str, bool], conjunction_states: dict[str, list[tuple[str, bool]]], depth: int):
    # if not any(conjunction_states.values()) and module.variable != "broadcast":
    #     return
    # if depth > 5:
    #     return
    
    # print(f"for module {module.variable} got pulse {"high" if pulse else "low"}")
    
    next_modules = []
    
    for module_name in module.destinations:
        if not module_name in modules:
            print(f"{module.variable} -{"high" if pulse else "low"}-> {module_name}")
            return
        
        new_module = modules[module_name]
        print(f"{module.variable} -{"high" if pulse else "low"}-> {new_module.variable}")
        match new_module.type:
            case ModuleType.Normal:
                new_pulse = pulse
            case ModuleType.FlipFlop:
                if not pulse:
                    old_state = flip_flop_states[new_module.variable]
                    new_state = not old_state
                    flip_flop_states[new_module.variable] = new_state
                    
                    if old_state:
                        new_pulse = False
                    else:
                        new_pulse = True
                else:
                    print(f"%{module.variable} -{"high" if pulse else "low"}-> {new_module.variable}")
                    return
            case ModuleType.Conjunction:
                state_list = conjunction_states[new_module.variable]
                for i, state in enumerate(state_list):
                    if state[0] == module.variable:
                        state_list[i] = (state[0], pulse)
                
                if all(state[1] for state in state_list):
                    new_pulse = False
                else:
                    new_pulse = True
    

        next_modules.append((new_module, new_pulse))

    # print("next", [x[0].variable for x in next_modules])
    for next_module in next_modules:
        calculate_pulses_recursive(next_module[0], next_module[1], map, flip_flop_states, conjunction_states, depth + 1)
    
    pass

def calculate_pulses(modules: dict[str, Module]):
    flip_flop_states: dict[str, bool] = { value.variable: False for value in modules.values() if value.type == ModuleType.FlipFlop }
    conjunction_states: dict[str, list[tuple[str, bool]]] = { value.variable: [(input, False) for input in modules if value.variable in modules[input].destinations] for value in modules.values() if value.type == ModuleType.Conjunction }
    
    start_module = modules["broadcaster"]
    start_pulse = False
    
    print(f"button -{"high" if start_pulse else "low"}-> {start_module.variable}")
    calculate_pulses_recursive(start_module, start_pulse, modules, flip_flop_states, conjunction_states, 0)
    
    pass



print(f"{calculate_pulses(modules)=}")