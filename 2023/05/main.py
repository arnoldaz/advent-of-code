from typing import NamedTuple, Optional

file_name = "input.txt"
with open(file_name) as file:
    lines = [line.rstrip() for line in file]

class SeedMap(NamedTuple):
    destination_start: int
    source_start: int
    range: int

seed_to_soil: list[SeedMap] = []
soil_to_fertilizer: list[SeedMap] = []
fertilizer_to_water: list[SeedMap] = []
water_to_light: list[SeedMap] = []
light_to_temperature: list[SeedMap] = []
temperature_to_humidity: list[SeedMap] = []
humidity_to_location: list[SeedMap] = []

seeds = [int(x) for x in lines[0].removeprefix("seeds: ").split(" ")]
i = 2
while i < len(lines):
    line = lines[i]
    if not line:
        i += 1
        continue

    match line:
        case "seed-to-soil map:":
            i += 1
            line = lines[i]
            while line:
                numbers = [int(x) for x in line.split(" ")]
                seed_to_soil.append(SeedMap(*numbers))
                i += 1
                line = lines[i] if i < len(lines) else ""
        case "soil-to-fertilizer map:":
            i += 1
            line = lines[i]
            while line:
                numbers = [int(x) for x in line.split(" ")]
                soil_to_fertilizer.append(SeedMap(*numbers))
                i += 1
                line = lines[i] if i < len(lines) else ""
        case "fertilizer-to-water map:":
            i += 1
            line = lines[i]
            while line:
                numbers = [int(x) for x in line.split(" ")]
                fertilizer_to_water.append(SeedMap(*numbers))
                i += 1
                line = lines[i] if i < len(lines) else ""
        case "water-to-light map:":
            i += 1
            line = lines[i]
            while line:
                numbers = [int(x) for x in line.split(" ")]
                water_to_light.append(SeedMap(*numbers))
                i += 1
                line = lines[i] if i < len(lines) else "" 
        case "light-to-temperature map:":
            i += 1
            line = lines[i]
            while line:
                numbers = [int(x) for x in line.split(" ")]
                light_to_temperature.append(SeedMap(*numbers))
                i += 1
                line = lines[i] if i < len(lines) else ""
        case "temperature-to-humidity map:":
            i += 1
            line = lines[i]
            while line:
                numbers = [int(x) for x in line.split(" ")]
                temperature_to_humidity.append(SeedMap(*numbers))
                i += 1
                line = lines[i] if i < len(lines) else ""
        case "humidity-to-location map:":
            i += 1
            line = lines[i]
            while line:
                numbers = [int(x) for x in line.split(" ")]
                humidity_to_location.append(SeedMap(*numbers))
                i += 1
                line = lines[i] if i < len(lines) else ""

def perform_mapping(seeds: list[int], map: list[SeedMap]) -> list[int]:
    results = []
    for seed in seeds:
        found_map = False
        for map_range in map:
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

def get_map_group_min(seeds: list[int], seed_to_soil: list[SeedMap], soil_to_fertilizer: list[SeedMap], fertilizer_to_water: list[SeedMap], 
    water_to_light: list[SeedMap], light_to_temperature: list[SeedMap], temperature_to_humidity: list[SeedMap], humidity_to_location: list[SeedMap]) -> int:
    
    soils = perform_mapping(seeds, seed_to_soil)
    fertilizers = perform_mapping(soils, soil_to_fertilizer)
    waters = perform_mapping(fertilizers, fertilizer_to_water)
    lights = perform_mapping(waters, water_to_light)
    temperatures = perform_mapping(lights, light_to_temperature)
    humidities = perform_mapping(temperatures, temperature_to_humidity)
    locations = perform_mapping(humidities, humidity_to_location)

    return min(locations)

class Range(NamedTuple):
    start: int
    end: int

def find_overlap(range1: Range, range2: Range) -> Optional[Range]:
    start = max(range1.start, range2.start)
    end = min(range1.end, range2.end)

    return Range(start, end) if start <= end else None

def remove_overlapping_range(source_range: Range, range_to_cut: Range) -> list[Range]:
    # If range to cut is outside the source range, return just the source range itself
    if range_to_cut.end < source_range.start or range_to_cut.start > source_range.end:
        return [source_range]

    overlapping_start = max(range_to_cut.start, source_range.start)
    overlapping_end = min(range_to_cut.end, source_range.end)

    # Add multiple ranges depending on whether range to cut is at the start, middle or end of source range
    remaining_ranges: list[Range] = []

    if overlapping_start > source_range.start:
        remaining_ranges.append(Range(source_range.start, overlapping_start - 1))

    if overlapping_end < source_range.end:
        remaining_ranges.append(Range(overlapping_end + 1, source_range.end))

    return remaining_ranges

def split_ranges(original_ranges: list[Range], critical_ranges: list[Range]) -> list[Range]:
    # original_ranges = [Range(79, 92), Range(55, 150)]
    # critical_ranges = [Range(98, 99), Range(50, 95)]
    # result = [(79, 92), (55, 95), (96, 97), (98, 99), (100, 150)]
    
    modified_ranges = original_ranges[:]
    final_ranges = set()

    for critical_range in critical_ranges:
        for original_range in modified_ranges:
            overlap = find_overlap(original_range, critical_range)
            if not overlap:
                final_ranges.add(original_range)
            else:
                if original_range in final_ranges:
                    final_ranges.remove(original_range)
                
                final_ranges.add(overlap)
                final_ranges.update(remove_overlapping_range(original_range, overlap))

        modified_ranges = list(final_ranges)

    return list(final_ranges)

def range_in_range(outer_range: Range, inner_range: Range) -> bool:
    # Whether inner range is in outer range
    return outer_range.start <= inner_range.start <= inner_range.end <= outer_range.end

def perform_range_mapping(seed_ranges: list[Range], map: list[SeedMap]) -> list[Range]:
    mapping_start_ranges = [Range(x.source_start, x.source_start + x.range - 1) for x in map]
    mapping_destination_ranges = [Range(x.destination_start, x.destination_start + x.range - 1) for x in map]

    split_seed_ranges = split_ranges(seed_ranges, mapping_start_ranges)
    mapped_seed_ranges: list[Range] = []

    for seed_range in split_seed_ranges:
        for i, mapping_range in enumerate(mapping_start_ranges):
            if range_in_range(mapping_range, seed_range):
                mapping_destination_range = mapping_destination_ranges[i]
                destination_start = seed_range.start - mapping_range.start + mapping_destination_range.start
                destination_end = seed_range.end - mapping_range.end + mapping_destination_range.end

                mapped_seed_ranges.append(Range(destination_start, destination_end))
                break
        else:
            mapped_seed_ranges.append(seed_range)

    return mapped_seed_ranges

def get_map_group_ranges_min(seeds: list[Range], seed_to_soil: list[SeedMap], soil_to_fertilizer: list[SeedMap], fertilizer_to_water: list[SeedMap], 
    water_to_light: list[SeedMap], light_to_temperature: list[SeedMap], temperature_to_humidity: list[SeedMap], humidity_to_location: list[SeedMap]) -> int:
    
    soils = perform_range_mapping(seeds, seed_to_soil)
    fertilizers = perform_range_mapping(soils, soil_to_fertilizer)
    waters = perform_range_mapping(fertilizers, fertilizer_to_water)
    lights = perform_range_mapping(waters, water_to_light)
    temperatures = perform_range_mapping(lights, light_to_temperature)
    humidities = perform_range_mapping(temperatures, temperature_to_humidity)
    locations = perform_range_mapping(humidities, humidity_to_location)

    return min([x.start for x in locations])

new_seed_ranges: list[Range] = []
for i in range(0, len(seeds), 2):
    new_seed_ranges.append(Range(seeds[i], seeds[i] + seeds[i+1] - 1))

print(f"{get_map_group_min(seeds, seed_to_soil, soil_to_fertilizer, fertilizer_to_water, water_to_light, light_to_temperature, temperature_to_humidity, humidity_to_location)=}")
print(f"{get_map_group_ranges_min(new_seed_ranges, seed_to_soil, soil_to_fertilizer, fertilizer_to_water, water_to_light, light_to_temperature, temperature_to_humidity, humidity_to_location)=}")
