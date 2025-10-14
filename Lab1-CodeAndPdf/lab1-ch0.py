import multiprocessing

def local_prefix(args):
    chunk, offset = args
    total = offset
    prefix = []
    for x in chunk:
        total += x
        prefix.append(total)
    return prefix, total

def MAIN(A):
    n = len(A)
    # Số tiến trình hợp lý (quá nhiều tiến trình làm chậm!)
    num_workers = min(8, multiprocessing.cpu_count(), (n + 99999)//100000)
    chunk_size = (n + num_workers - 1) // num_workers
    chunks = [A[i:i+chunk_size] for i in range(0, n, chunk_size)]

    # Tính tổng từng chunk tuần tự để lấy offset
    offsets = [0]
    sums = []
    for chunk in chunks:
        sums.append(sum(chunk))
    for i in range(1, len(sums)):
        offsets.append(offsets[i-1] + sums[i-1])

    # Gán offset cho từng chunk
    tasks = list(zip(chunks, offsets))

    # Song song hóa tính prefix từng chunk
    with multiprocessing.Pool(num_workers) as pool:
        partial = pool.map(local_prefix, tasks)

    # Ghép kết quả
    result = []
    for prefix, _ in partial:
        result.extend(prefix)
    return result