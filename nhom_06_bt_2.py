import random
import multiprocessing

def compute_size(subarr):
    return len(subarr)

def prefix_sum(arr):
    psum = [0] * len(arr)
    total = 0
    for i in range(len(arr)):
        psum[i] = total
        total += arr[i]
    return psum

def copy_to_result(task):
    i, A_i, offset = task
    return (offset, A_i)

if __name__ == "__main__":
    # Tạo A gồm 1000 mảng nhỏ, mỗi mảng có 1000 số ngẫu nhiên
    A = [[random.randint(1, 100) for _ in range(1000)] for _ in range(1000)]

    # Bước 1: Tính size từng mảng con (S)
    with multiprocessing.Pool() as pool:
        S = pool.map(compute_size, A)

    # Bước 2: Tính offset bằng prefix sum
    offset = prefix_sum(S)
    total_len = offset[-1] + S[-1]

    # Bước 3: Dùng pool để chép từng mảng con vào kết quả
    tasks = [(i, A[i], offset[i]) for i in range(len(A))]
    B = [0] * total_len

    with multiprocessing.Pool() as pool:
        results = pool.map(copy_to_result, tasks)

    for off, subarr in results:
        B[off : off + len(subarr)] = subarr

    # In ra [X, Y, Z]
    print([B[0], B[-1], len(B)])
