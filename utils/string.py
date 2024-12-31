import re

def nearly_equal(first: str | list[str], second: str | list[str]) -> bool:
    """Checks whether the strings only differ by 1 character"""
    count_diffs = 0
    for a, b in zip(first, second):
        if a == b:
            continue

        if count_diffs > 1:
            return False

        count_diffs += 1

    return count_diffs == 1

def get_ints(string: str, allow_negative: bool = False) -> list[int]:
    """Gets all integers from a string using regex"""
    regex = r"\d+" if not allow_negative else r"-*\d+"
    return [int(x) for x in re.findall(regex, string)]
