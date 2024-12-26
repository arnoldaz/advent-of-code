import json
import re

def silver_solution(lines: list[str]) -> int:
    return sum(int(x) for x in re.findall(r"-?\d+", lines[0]))

def gold_solution(lines: list[str]) -> int:
    filtered_out_red = str(json.loads(lines[0], object_hook=lambda obj: obj if "red" not in obj.values() else {}))
    return sum(int(x) for x in re.findall(r"-?\d+", filtered_out_red))
