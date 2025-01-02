# pylint: disable-all

import sys

from utils.string import replace_nth_instance


def parse_input(lines: list[str]):
    replacements: dict[str, list[str]] = {}
    empty_line = lines.index("")

    replacements_list: list[tuple[str, str]] = []

    for line in lines[:empty_line]:
        key, value = line.split(" => ")
        replacements_list.append((key, value))
        replacements.setdefault(key, []).append(value)

    return replacements, lines[empty_line + 1], replacements_list

def parse_input2(lines: list[str]):
    replacements: dict[str, str] = {}
    empty_line = lines.index("")

    replacements_list: list[tuple[str, str]] = []

    for line in lines[:empty_line]:
        key, value = line.split(" => ")
        replacements_list.append((value, key))
        replacements[value] = key

    return replacements, lines[empty_line + 1], replacements_list

def Nreplacer(string,srch,rplc,n):
    Sstring = string.split(srch)
    #first check if substring is even present n times
    #then paste the part before the nth substring to the part after the nth substring
    #, with the replacement inbetween
    if len(Sstring) > (n):
        return f'{srch.join(Sstring[:(n)])}{rplc}{srch.join(Sstring[n:])}' 
    else:
        return string

def replaceNth(s, source, target, n):
    inds = [i for i in range(len(s) - len(source)+1) if s[i:i+len(source)]==source]
    print("inds", inds)
    if len(inds) < n:
        return "" # or maybe raise an error
    s = list(s)  # can't assign to string slices. So, let's listify
    s[inds[n-1]:inds[n-1]+len(source)] = target  # do n-1 because we start from the first occurrence of the string, not the 0-th
    return ''.join(s)

def silver_solution(lines: list[str]) -> int:
    replacements, molecule, replacements_list = parse_input(lines)

    unique_strings = set[str]()

    for s1, s2 in replacements_list:
        if s1 in molecule:
            for x in range(1, molecule.count(s1)+1):
                # molecule.find()
                new = replace_nth_instance(molecule, s1, s2, x)
                unique_strings.add(new)
            # x = molecule.replace(s1, s2, 1)
            # unique_strings.add(x)

    # print(unique_strings)

    # for x in unique_strings:
    #     print(x)

    return len(unique_strings)

def recurse(current_molecule: str, final_molecule: str, replacements: dict[str, list[str]], count: int):
    # print("start of recurse", current_molecule, count)

    if current_molecule == final_molecule:
        print("OOOOASASASHKJAS")
        return count

    if len(current_molecule) > len(final_molecule) or count > 100:
        return sys.maxsize

    # print(count, len(current_molecule), len(final_molecule), current_molecule)

    min_count = sys.maxsize
    for key, values in replacements.items():
        for value in values:
            if key in current_molecule:
                for x in range(1, current_molecule.count(key)+1):
                    new = current_molecule.replace(key, value, x)
                    # print(new, new in final_molecule)

                    possible_min = recurse(new, final_molecule, replacements, count + 1)
                    min_count = min(possible_min, min_count)

    return min_count

def find_shortest_replacement(current_mol: str, final_mol: str, replacements: list[tuple[str, str]], count: int):
    # print(current_mol, final_mol, count)
    
    if current_mol == final_mol:
        # print("WOOOOOOOOOOOOOOOOOOOOW", count)
        return count
    
    for key, value in replacements:
        if key in current_mol:
            # print("REPLACED", key, value, replacements.index((key, value)))
            new = current_mol.replace(key, value, 1)
            possible_min = find_shortest_replacement(new, final_mol, replacements, count + 1)
            return possible_min

    return -1

def gold_solution(lines: list[str]) -> int:
    replacements, molecule, replacements_list = parse_input2(lines)


    replacements_list.sort(key=lambda x: len(x[0]), reverse=True)

    # for x in replacements_list:
    #     print(x)

    a = find_shortest_replacement(molecule, "e", replacements_list, 0)

    # print(a)

    return a
