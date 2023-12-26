
def remove_list_indexes(list: list, indexes_to_remove: list[int]):
    for item in sorted(indexes_to_remove, reverse=True): 
        del list[item]
