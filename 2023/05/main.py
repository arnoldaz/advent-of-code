from typing import NamedTuple

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

print(f"{get_map_group_min(seeds, seed_to_soil, soil_to_fertilizer, fertilizer_to_water, water_to_light, light_to_temperature, temperature_to_humidity, humidity_to_location)=}")