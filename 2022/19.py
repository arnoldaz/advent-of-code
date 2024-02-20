# pylint: disable=unused-argument

import re
from typing import NamedTuple

class Blueprint(NamedTuple):
    id: int
    ore_cost: int
    clay_cost: int
    obsidian_cost: tuple[int, int]
    geode_cost: tuple[int, int]

def parse_input(lines: list[str]):
    blueprints: list[Blueprint] = []

    blueprint_format = r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian."
    for line in lines:
        match = re.match(blueprint_format, line)
        if not match:
            continue

        blueprints.append(Blueprint(int(match.group(1)), int(match.group(2)), int(match.group(3)), (int(match.group(4)), int(match.group(5))), (int(match.group(6)), int(match.group(7)))))

    return blueprints

def find_max_geode_count(blueprint: Blueprint) -> int:
    minutes_left = 24

    ore = 0
    clay = 0
    obsidian = 0
    geode = 0

    ore_robot = 1
    clay_robot = 0
    obsidian_robot = 0
    geode_robot = 0

    while minutes_left > 0:
        initial_ore_robot = ore_robot
        initial_clay_robot = clay_robot
        initial_obsidian_robot = obsidian_robot
        initial_geode_robot = geode_robot

        needed_ore, needed_obsidian = blueprint.geode_cost
        if ore >= needed_ore and obsidian >= needed_obsidian:
            geode_robot += 1
            ore -= needed_ore
            obsidian -= needed_obsidian

        needed_ore, needed_clay = blueprint.obsidian_cost
        if ore >= needed_ore and clay >= needed_clay:
            obsidian_robot += 1
            ore -= needed_ore
            clay -= needed_clay

        needed_ore = blueprint.clay_cost
        if ore >= needed_ore:
            clay_robot += 1
            ore -= needed_ore

        ore += initial_ore_robot
        clay += initial_clay_robot
        obsidian += initial_obsidian_robot
        geode += initial_geode_robot

        minutes_left -= 1

    print(ore, clay, obsidian, geode)

    return geode

def silver_solution(lines: list[str]) -> int:
    blueprints = parse_input(lines)

    # return sum(blueprint.id * find_max_geode_count(blueprint) for blueprint in blueprints)

    answer = 0
    for blueprint in blueprints:
        count = find_max_geode_count(blueprint)
        print(f"ID: {blueprint.id} | geode count: {count}")
        answer += blueprint.id * count

    return answer

def gold_solution(lines: list[str]) -> int:
    # Implement solution
    return -321
