from utils.string import replace_nth_instance

def parse_input(lines: list[str]):
    empty_line = lines.index("")
    replacements = [tuple[str, str](line.split(" => ")) for line in lines[:empty_line]]

    return replacements, lines[empty_line + 1]

def find_shortest_replacement(current_molecule: str, final_molecule: str, replacements: list[tuple[str, str]], count: int):
    if current_molecule == final_molecule:
        return count

    for key, value in replacements:
        if value in current_molecule:
            new_molecule = current_molecule.replace(value, key, 1)
            return find_shortest_replacement(new_molecule, final_molecule, replacements, count + 1)

    return -1

def silver_solution(lines: list[str]) -> int:
    replacements, molecule = parse_input(lines)
    unique_strings = set[str]()

    for key, value in replacements:
        if key in molecule:
            for n in range(molecule.count(key)):
                unique_strings.add(replace_nth_instance(molecule, key, value, n + 1))

    return len(unique_strings)

def gold_solution(lines: list[str]) -> int:
    replacements, molecule = parse_input(lines)
    replacements.sort(key=lambda x: len(x[0]), reverse=True)

    return find_shortest_replacement(molecule, "e", replacements, 0)
