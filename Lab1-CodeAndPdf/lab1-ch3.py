from concurrent.futures import ProcessPoolExecutor

def merge_two(a, b):
    i, j = 0, 0
    merged = []
    while i < len(a) and j < len(b):
        if a[i] < b[j]:
            merged.append(a[i])
            i += 1
        else:
            merged.append(b[j])
            j += 1
    merged.extend(a[i:])
    merged.extend(b[j:])
    return merged

def parallel_sort(arr):
    if len(arr) <= 100000:
        return sorted(arr)
    n = len(arr)
    num_chunks = 4
    chunk_size = (n + num_chunks - 1) // num_chunks
    chunks = [arr[i:i+chunk_size] for i in range(0, n, chunk_size)]
    with ProcessPoolExecutor(max_workers=num_chunks) as executor:
        sorted_chunks = list(executor.map(sorted, chunks))
    # Merge 4 mảng đã sort
    merged = merge_two(sorted_chunks[0], sorted_chunks[1])
    merged = merge_two(merged, sorted_chunks[2])
    merged = merge_two(merged, sorted_chunks[3])
    return merged

def MAIN(arrayA):
    return parallel_sort(arrayA)