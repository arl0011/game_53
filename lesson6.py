
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def binary_search(arr, val):
    first = 0
    last = len(arr) - 1
    result_ok = False
    pos = -1

    while first <= last:
        middle = (first + last) // 2
        if val == arr[middle]:
            result_ok = True
            pos = middle
            break
        elif val > arr[middle]:
            first = middle + 1
        else:
            last = middle - 1

    if result_ok:
        print(f"Элемент найден на позиции: {pos}")
    else:
        print("Элемент не найден")


# Пример использования:
unsorted_list = [42, 15, 7, 88, 3, 91, 23, 31, 67, 55]
print("Исходный список:", unsorted_list)

sorted_list = bubble_sort(unsorted_list)
print("Отсортированный список:", sorted_list)


binary_search(sorted_list, 31)
binary_search(sorted_list, 100)