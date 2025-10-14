import multiprocessing

# Hàm tính tổng prefix sum trong một đoạn [start, end)
def scan_recursive(arr, start, end, offset, result):
    if end - start == 1:
        result[start] = arr[start] + offset
        return arr[start]

    mid = (start + end) // 2
    left_sum = scan_recursive(arr, start, mid, offset, result)
    right_sum = scan_recursive(arr, mid, end, offset + left_sum, result)
    return left_sum + right_sum

def parallel_prefix_sum(arr):
    n = len(arr)
    result = multiprocessing.Array('i', n)  # mảng dùng chung giữa các tiến trình

    # Để tránh multiprocessing phức tạp, gọi đệ quy trên một tiến trình chính
    scan_recursive(arr, 0, n, 0, result)

    return list(result)

if __name__ == "__main__":
    # Mảng đầu vào: 1, 2, 3, ..., 1000
    a = list(range(1, 1001))
    prefix_sum_result = parallel_prefix_sum(a)

    print("Prefix Sum Result:")
    print(prefix_sum_result)
