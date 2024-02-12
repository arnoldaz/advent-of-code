import queue
import re
from typing import Callable, NamedTuple, TypeVar

class ValveData(NamedTuple):
    flow_rate: int
    tunnels: list[str]

def parse_input(lines: list[str]) -> dict[str, ValveData]:
    valves: dict[str, ValveData] = {}

    line_format = r"^Valve ([A-Z]+) has flow rate=(\d+); tunnels* leads* to valves* ([A-Z\,\s]+)$"
    for line in lines:
        match = re.match(line_format, line)
        if not match:
            continue

        valve_name = match.group(1)
        flow_rate = int(match.group(2))
        tunnels = match.group(3).split(", ")
        valves[valve_name] = ValveData(flow_rate, tunnels)

    return valves

def get_paths_bfs(valves: dict[str, ValveData], start_valve: str, end_valves: list[str]) -> list[list[str]]:
    frontier = queue.Queue[tuple[str, list[str]]]()
    frontier.put((start_valve, []))
    visited = set([start_valve])
    all_paths: list[list[str]] = []

    while not frontier.empty():
        current, path = frontier.get()
        for neighbor in valves[current].tunnels:
            if neighbor not in visited:
                visited.add(neighbor)
                new_path = path + [neighbor]
                frontier.put((neighbor, new_path))
                if neighbor in end_valves:
                    all_paths.append(new_path)

    return all_paths

class ValvePath:
    MAX_TIMER = 30

    def __init__(self, position: str, valves: dict[str, ValveData]):
        self.position = position
        self.valves = valves
        self.open_valves: list[str] = []
        self.total_pressure = 0
        self.timer = 1

    def clone(self) -> "ValvePath":
        clone = ValvePath(self.position, self.valves)
        clone.open_valves = self.open_valves[:]
        clone.total_pressure = self.total_pressure
        clone.timer = self.timer
        return clone

    def update_flow(self):
        if self.timer > self.MAX_TIMER:
            return

        for open_valve in self.open_valves:
            self.total_pressure += self.valves[open_valve].flow_rate

    def move(self, path: list[str]):
        if self.timer > self.MAX_TIMER:
            return

        # move to valve through the path
        for checkpoint in path:
            self.update_flow()
            self.position = checkpoint
            self.timer += 1

            if self.timer > self.MAX_TIMER:
                return

        # open it
        self.update_flow()
        self.open_valves.append(path[-1])
        self.timer += 1

    def pass_time(self):
        while self.timer <= self.MAX_TIMER:
            self.update_flow()
            self.timer += 1

T = TypeVar("T")
def partition(predicate: Callable[[T], bool], iterable: list[T]) -> tuple[list[T], list[T]]:
    trues = []
    falses = []
    for item in iterable:
        if predicate(item):
            trues.append(item)
        else:
            falses.append(item)
    return trues, falses

def navigate_path(valves: dict[str, ValveData]):
    good_valves = [name for name, data in valves.items() if data.flow_rate > 0]
    start_valve = "AA"

    valve_paths: list[ValvePath] = [ValvePath(start_valve, valves)]

    max_value = 0

    while True:
        print("before", len(valve_paths))
        valve_paths, finished_valve_paths = partition(lambda x: x.timer <= ValvePath.MAX_TIMER, valve_paths)
        print("after", len(valve_paths))

        if len(finished_valve_paths) > 0:
            max_value = max(max(x.total_pressure for x in finished_valve_paths), max_value)

        if len(valve_paths) == 0:
            break

        for valve_path in valve_paths[:]:
            destinations = [x for x in good_valves if x not in valve_path.open_valves]
            paths = get_paths_bfs(valves, valve_path.position, destinations)

            if len(paths) == 0:
                valve_path.pass_time()
                continue

            # clone and move 1 to n
            for i in range(1, len(paths)):
                clone = valve_path.clone()
                clone.move(paths[i])
                valve_paths.append(clone)

            # move 0
            valve_path.move(paths[0])

    # valve_paths.sort(key=lambda x: x.total_pressure, reverse=True)
    # for path in valve_paths[:]:
    #     print(path.position, path.open_valves, path.total_pressure, path.timer)

    return max_value

def silver_solution(lines: list[str]) -> int:
    valves = parse_input(lines)
    return navigate_path(valves)


def gold_solution(_lines: list[str]) -> int:
    return -321
