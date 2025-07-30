def linear_search(array, element):
    for index, value in enumerate(array):
        if value == element:
            return index
    return -1