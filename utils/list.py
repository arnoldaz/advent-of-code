
def remove_list_indexes(list_to_check: list, indexes_to_remove: list[int]):
    for item in sorted(indexes_to_remove, reverse=True):
        del list_to_check[item]

def two_largest(list_to_check: list[int]) -> tuple[int, int]:
    largest = -1
    largest_index = -1
    second_largest = -1

    for i, item in enumerate(list_to_check):
        if item > largest:
            second_largest = largest
            largest = item
            largest_index = i
        elif largest >= item > second_largest and largest_index != i:
            second_largest = item

    return largest, second_largest
