import random
from concurrent.futures import ProcessPoolExecutor
import multiprocessing

# Thuật toán QuickSort song song
def parallel_quicksort(arr, depth=0):
    if len(arr) <= 1:
        return arr
    if depth >= 2: 
        return sorted(arr)

    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    with ProcessPoolExecutor(max_workers=2) as executor:
        left_future = executor.submit(parallel_quicksort, left, depth + 1)
        right_future = executor.submit(parallel_quicksort, right, depth + 1)
        sorted_left = left_future.result()
        sorted_right = right_future.result()

    return sorted_left + middle + sorted_right

def MAIN():
    random.seed(42)
    arr = [random.randint(1, 10000) for _ in range(1000)]

    multiprocessing.set_start_method("fork", force=True)
    sorted_arr = parallel_quicksort(arr)

    print([sorted_arr[0], sorted_arr[-1]])

if __name__ == '__main__':
    MAIN()