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

class ValveDualPath:
    MAX_TIMER = 10

    def __init__(self, position1: str, position2: str, valves: dict[str, ValveData], good_valves: list[str]):
        self.position1 = position1
        self.position2 = position2

        self.current_path1: list[str] = []
        self.current_path2: list[str] = []

        self.just_arrived1 = False
        self.just_arrived2 = False

        self.valves = valves
        self.open_valves = set[str]()
        self.total_pressure = 0
        self.timer = 1

        self.good_valves = good_valves

    def clone(self) -> "ValveDualPath":
        clone = ValveDualPath(self.position1, self.position2, self.valves, self.good_valves)
        clone.open_valves = self.open_valves.copy()
        clone.total_pressure = self.total_pressure
        clone.timer = self.timer
        clone.current_path1 = self.current_path1[:]
        clone.current_path2 = self.current_path2[:]
        clone.just_arrived1 = self.just_arrived1
        clone.just_arrived2 = self.just_arrived2
        return clone

    def update_flow(self):
        if self.timer > self.MAX_TIMER:
            return

        for open_valve in self.open_valves:
            self.total_pressure += self.valves[open_valve].flow_rate

    def move_minute(self) -> list["ValveDualPath"]:
        if self.timer > self.MAX_TIMER:
            return []

        self.update_flow()
        self.timer += 1

        destinations = [x for x in self.good_valves if x not in self.open_valves]

        paths1: list[list[str]] = []
        paths2: list[list[str]] = []

        # player 1

        # move through current path
        if len(self.current_path1) > 0:
            next_segment = self.current_path1.pop()
            self.position1 = next_segment
            self.just_arrived1 = True
        else:
            # arrived to finish last minute
            if self.just_arrived1:
                self.open_valves.add(self.position1)
                self.just_arrived1 = False
            # arrived ant turned on, need to find new target
            else:
                destinations = [x for x in self.good_valves if x not in self.open_valves and (len(self.current_path2) == 0 or x != self.current_path2[0])]
                paths1 = get_paths_bfs(self.valves, self.position1, destinations)
                paths1.reverse()

        # player 2

        # move through current path
        if len(self.current_path2) > 0:
            next_segment = self.current_path2.pop()
            self.position2 = next_segment
            self.just_arrived2 = True
        else:
            # arrived to finish last minute
            if self.just_arrived2:
                self.open_valves.add(self.position2)
                self.just_arrived2 = False
            # arrived ant turned on, need to find new target
            else:
                destinations = [x for x in self.good_valves if x not in self.open_valves and (len(self.current_path1) == 0 or x != self.current_path1[0])]
                paths2 = get_paths_bfs(self.valves, self.position2, destinations)
                paths2.reverse()

        if len(paths1) > 0 and len(paths2) > 0:
            result: list[ValveDualPath] = []
            for path1 in paths1:
                for path2 in paths2:
                    if path1 == path2:
                        continue
                    new_valve_path = self.clone()
                    new_valve_path.current_path1 = path1
                    new_valve_path.current_path2 = path2
                    result.append(new_valve_path)

            self.current_path1 = result[0].current_path1
            self.current_path2 = result[0].current_path2
            return result[1:]
        elif len(paths1) > 0:
            result: list[ValveDualPath] = []
            for path in paths1:
                new_valve_path = self.clone()
                new_valve_path.current_path1 = path
                result.append(new_valve_path)

            self.current_path1 = result[0].current_path1
            return result[1:]
        elif len(paths2) > 0:
            result: list[ValveDualPath] = []
            for path in paths2:
                new_valve_path = self.clone()
                new_valve_path.current_path2 = path
                result.append(new_valve_path)

            self.current_path2 = result[0].current_path2
            return result[1:]
        else:
            return []

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

    counter = 0

    while True:
        print("before", len(valve_paths))
        valve_paths, finished_valve_paths = partition(lambda x: x.timer <= ValvePath.MAX_TIMER, valve_paths)
        print("after", len(valve_paths))

        if len(finished_valve_paths) > 0:
            counter += len(finished_valve_paths)
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

    print("counter", counter)

    return max_value

def navigate_path_gold(valves: dict[str, ValveData]):
    good_valves = [name for name, data in valves.items() if data.flow_rate > 0]
    start_valve = "AA"

    valve_paths: list[ValveDualPath] = [ValveDualPath(start_valve, start_valve, valves, good_valves)]

    max_value = 0

    while True:
        print("before", len(valve_paths))
        valve_paths, finished_valve_paths = partition(lambda x: x.timer <= ValveDualPath.MAX_TIMER, valve_paths)
        print("after", len(valve_paths))

        if len(finished_valve_paths) > 0:
            max_value = max(max(x.total_pressure for x in finished_valve_paths), max_value)

        if len(valve_paths) == 0:
            break

        # paths_to_remove: list[int] = []

        for valve_path in valve_paths[:]:
            more_paths = valve_path.move_minute()
            valve_paths += more_paths
            # paths_to_remove.append(i)

        # remove_list_indexes(valve_paths, paths_to_remove)

    return max_value

def silver_solution(lines: list[str]) -> int:
    valves = parse_input(lines)
    return navigate_path(valves)

def gold_solution(lines: list[str]) -> int:
    valves = parse_input(lines)
    return navigate_path_gold(valves)
