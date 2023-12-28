
def remove_list_indexes(list: list, indexes_to_remove: list[int]):
    for item in sorted(indexes_to_remove, reverse=True): 
        del list[item]

def two_largest(list: list[int]) -> tuple[int, int]:
    largest = -1
    largest_index = -1
    second_largest = -1

    for i, item in enumerate(list):
        if item > largest:
            second_largest = largest
            largest = item
            largest_index = i
        elif largest >= item > second_largest and largest_index != i:
            second_largest = item

    return largest, second_largest