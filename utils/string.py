
# checks whether strings differ by 1 character
def nearly_equal(string1: str | list[str], string2: str | list[str]) -> bool:
    count_diffs = 0
    for a, b in zip(string1, string2):
        if a == b:
            continue

        if count_diffs > 1:
            return False

        count_diffs += 1

    return count_diffs == 1
