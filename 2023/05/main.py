from typing import NamedTuple

file_name = "input-test.txt"
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

print(f"{get_map_group_min(seeds, seed_to_soil, soil_to_fertilizer, fertilizer_to_water, water_to_light, light_to_temperature, temperature_to_humidity, humidity_to_location)=}")

new_seed_ranges: list[tuple[int, int]] = []
for i in range(0, len(seeds), 2):
    new_seed_ranges.append((seeds[i], seeds[i] + seeds[i+1] - 1))

new_seed_ranges=[(79, 92), (55, 150)]
print(f"{new_seed_ranges=}")

new_seed_to_soil = [(x.source_start, x.source_start + x.range - 1) for x in seed_to_soil]
new_seed_to_soil=[(98, 99), (50, 95)]
print(f"{new_seed_to_soil=}")

# new_soil_to_fertilizer = [(x.source_start, x.source_start + x.range - 1) for x in soil_to_fertilizer]
# print(f"{new_soil_to_fertilizer=}")
# new_soil_to_fertilizer=[(15, 51), (52, 53), (0, 14)]

result = [(79, 92), (55, 95), (96, 97), (98, 99), (100, 150)]

split_seed_ranges = []
for seed in new_seed_ranges:
    for soil_map in new_seed_to_soil:
        if seed[0] <= soil_map[0] <= seed[1]:
            split_seed_ranges.append(soil_map[0])
        if seed[0] <= soil_map[1] <= seed[1]:
            split_seed_ranges.append(soil_map[1])


print(split_seed_ranges)

# seed  soil
# 0     0
# 1     1
# ...   ...
# 48    48
# 49    49
# 50    52
# 51    53
# ...   ...
# 96    98
# 97    99
# 98    50
# 99    51

