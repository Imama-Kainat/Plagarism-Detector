def bubble_sort(data):
    size = len(data)
    for i in range(size):
        for j in range(0, size - i - 1):
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
    return data