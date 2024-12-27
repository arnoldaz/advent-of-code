import re
from typing import NamedTuple

class Aunt(NamedTuple):
    number: int
    data: dict[str, int]

def parse_input(lines: list[str]) -> list[Aunt]:
    line_regex = r"Sue (\d+): (\w+): (\d+), (\w+): (\d+), (\w+): (\d+)"
    aunts: list[Aunt] = []
    for line in lines:
        matches = re.match(line_regex, line)
        assert matches is not None
        number, key1, value1, key2, value2, key3, value3 = matches.groups()
        aunts.append(
            Aunt(int(number), {key1: int(value1), key2: int(value2), key3: int(value3)})
        )

    return aunts

def get_expected_aunt_data() -> dict[str, int]:
    return {
        "children": 3,
        "cats": 7,
        "samoyeds": 2,
        "pomeranians": 3,
        "akitas": 0,
        "vizslas": 0,
        "goldfish": 5,
        "trees": 3,
        "cars": 2,
        "perfumes": 1,
    }

def silver_solution(lines: list[str]) -> int:
    aunts = parse_input(lines)
    expected_data = get_expected_aunt_data()

    return next(
        aunt.number
        for aunt in aunts
        if all(aunt.data[key] == expected_data[key] for key in aunt.data.keys())
    )

def gold_solution(lines: list[str]) -> int:
    aunts = parse_input(lines)
    expected_data = get_expected_aunt_data()

    return next(
        aunt.number
        for aunt in aunts
        if all(
            (key in ("cats", "trees") and value > expected_data[key])
            or (key in ("pomeranians", "goldfish") and value < expected_data[key])
            or (key not in ("cats", "trees", "pomeranians", "goldfish") and value == expected_data[key])
            for key, value in aunt.data.items()
        )
    )
