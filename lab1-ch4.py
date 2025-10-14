import threading
from concurrent.futures import ThreadPoolExecutor

def read_numbers_from_file(filename):
    """Đọc tất cả số nguyên từ file và trả về dưới dạng mảng"""
    numbers = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                line_numbers = line.strip().split()
                for num_str in line_numbers:
                    if num_str:
                        numbers.append(int(num_str))
        return numbers
    except (FileNotFoundError, ValueError):
        return []

def sequential_search(arr, target):
    """Tìm kiếm tuần tự"""
    for i, num in enumerate(arr):
        if num == target:
            return i
    return -1

def parallel_search_chunk(arr, target, start_idx, end_idx, result_dict, thread_id):
    """Tìm kiếm một phần của mảng bằng thread"""
    for i in range(start_idx, end_idx):
        if arr[i] == target:
            result_dict[thread_id] = i
            return
    result_dict[thread_id] = -1

def parallel_search_with_threads(arr, target, num_threads=4):
    """Tìm kiếm song song bằng thread thủ công"""
    if not arr:
        return -1

    n = len(arr)
    chunk_size = n // num_threads
    threads = []
    result_dict = {}

    for i in range(num_threads):
        start_idx = i * chunk_size
        end_idx = n if i == num_threads - 1 else (i + 1) * chunk_size
        thread = threading.Thread(
            target=parallel_search_chunk,
            args=(arr, target, start_idx, end_idx, result_dict, i)
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    found_indices = [idx for idx in result_dict.values() if idx != -1]
    return min(found_indices) if found_indices else -1

def parallel_search_with_executor(arr, target, num_workers=4):
    """Tìm kiếm song song bằng ThreadPoolExecutor"""
    if not arr:
        return -1

    n = len(arr)
    chunk_size = n // num_workers

    def search_chunk(start_idx, end_idx):
        for i in range(start_idx, min(end_idx, n)):
            if arr[i] == target:
                return i
        return -1

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = []
        for i in range(num_workers):
            start_idx = i * chunk_size
            end_idx = n if i == num_workers - 1 else (i + 1) * chunk_size
            future = executor.submit(search_chunk, start_idx, end_idx)
            futures.append(future)

        results = []
        for future in futures:
            result = future.result()
            if result != -1:
                results.append(result)

        return min(results) if results else -1

def MAIN(input_file_path, key_value):
    """Hàm chính của bài tập - tìm kiếm số trong file"""
    numbers = read_numbers_from_file(input_file_path)
    if not numbers:
        return -1
    return parallel_search_with_threads(numbers, key_value, num_threads=4)