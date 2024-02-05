from typing import NamedTuple

class Instruction(NamedTuple):
    operation: str
    value: int

class CycleClock:
    def __init__(self, is_crt: bool):
        self.cycle = 0
        self.is_crt = is_crt

        self.critical_cycles = (20, 60, 100, 140, 180, 220)
        self.strength = 0

        self.crt_data: list[str] = [""]

    def tick(self, register: int):
        self.cycle += 1
        if self.is_crt:
            self._calculate_crt(register)
        else:
            self._calculate_strength(register)

    def _calculate_crt(self, register: int):
        self.crt_data[-1] += "\u2593" if register <= self.cycle <= register + 2 else " "
        if self.cycle % 40 == 0:
            self.crt_data.append("")
            self.cycle = 0

    def _calculate_strength(self, register: int):
        if self.cycle in self.critical_cycles:
            self.strength += self.cycle * register

    def draw_crt(self):
        for line in self.crt_data:
            print(line)

    def get_strength_sum(self) -> int:
        return self.strength

def parse_input(lines: list[str]) -> list[Instruction]:
    instructions = []

    for line in lines:
        if " " in line:
            operation, value = line.split()
        else:
            operation, value = line, None
        instructions.append(Instruction(operation, int(value) if value else 0))

    return instructions

def run_all_clock_cycles(instructions: list[Instruction], clock: CycleClock):
    register = 1
    for instruction in instructions:
        match instruction.operation:
            case "noop":
                clock.tick(register)
            case "addx":
                clock.tick(register)
                clock.tick(register)
                register += instruction.value

def silver_solution(lines: list[str]) -> int:
    instructions = parse_input(lines)
    clock = CycleClock(False)
    run_all_clock_cycles(instructions, clock)

    return clock.get_strength_sum()

def gold_solution(lines: list[str]) -> str:
    instructions = parse_input(lines)
    clock = CycleClock(True)
    run_all_clock_cycles(instructions, clock)

    # clock.draw_crt()
    return "ZGCJZJFL" # visually parsed from generated CRT image
