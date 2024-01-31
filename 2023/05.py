from typing import NamedTuple
from utils.ranges import Range, range_in_range, split_ranges

class SeedMap(NamedTuple):
    destination_start: int
    source_start: int
    range: int

def parse_input(lines: list[str]) -> tuple[list[int], list[list[SeedMap]]]:
    seed_maps: list[list[SeedMap]] = []
    current_seed_map: list[SeedMap] = []

    seeds = [int(x) for x in lines[0].removeprefix("seeds: ").split(" ")]
    for line in lines[1:]:
        if not line:
            continue

        if line.endswith("map:"):
            if len(current_seed_map) > 0:
                seed_maps.append(current_seed_map)
                current_seed_map = []
            continue

        numbers = [int(x) for x in line.split(" ")]
        current_seed_map.append(SeedMap(*numbers))

    if len(current_seed_map) > 0:
        seed_maps.append(current_seed_map)

    return seeds, seed_maps

def perform_mapping(seeds: list[int], seed_maps: list[SeedMap]) -> list[int]:
    results = []
    for seed in seeds:
        found_map = False
        for map_range in seed_maps:
            low_range = map_range.source_start
            high_range = map_range.source_start + map_range.range

            if high_range >= seed >= low_range:
                index = high_range - seed
                soil = map_range.destination_start + map_range.range - index
                results.append(soil)
                found_map = True
                break

        if not found_map:
            results.append(seed)

    return results

def perform_range_mapping(seed_ranges: list[Range], seed_maps: list[SeedMap]) -> list[Range]:
    mapping_start_ranges = [Range(x.source_start, x.source_start + x.range - 1) for x in seed_maps]
    mapping_destination_ranges = [Range(x.destination_start, x.destination_start + x.range - 1) for x in seed_maps]

    split_seed_ranges = split_ranges(seed_ranges, mapping_start_ranges)
    mapped_seed_ranges: list[Range] = []

    for seed_range in split_seed_ranges:
        for i, mapping_range in enumerate(mapping_start_ranges):
            if not range_in_range(mapping_range, seed_range):
                continue

            mapping_destination_range = mapping_destination_ranges[i]
            destination_start = seed_range.start - mapping_range.start + mapping_destination_range.start
            destination_end = seed_range.end - mapping_range.end + mapping_destination_range.end

            mapped_seed_ranges.append(Range(destination_start, destination_end))
            break
        else:
            mapped_seed_ranges.append(seed_range)

    return mapped_seed_ranges

def silver_solution(lines: list[str]) -> int:
    seeds, seed_maps = parse_input(lines)

    mapped_values = perform_mapping(seeds, seed_maps[0])
    for seed_map in seed_maps[1:]:
        mapped_values = perform_mapping(mapped_values[:], seed_map)

    return min(mapped_values)

def gold_solution(lines: list[str]) -> int:
    seeds, seed_maps = parse_input(lines)
    new_seed_ranges = [Range(seeds[i], seeds[i] + seeds[i+1] - 1) for i in range(0, len(seeds), 2)]

    mapped_values = perform_range_mapping(new_seed_ranges, seed_maps[0])
    for seed_map in seed_maps[1:]:
        mapped_values = perform_range_mapping(mapped_values[:], seed_map)

    return min(x.start for x in mapped_values)
