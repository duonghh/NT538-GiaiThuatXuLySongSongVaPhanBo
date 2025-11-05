from concurrent.futures import ProcessPoolExecutor

def multiply_rows(rows_a, matrix_b):
    n = len(matrix_b)
    result_rows = []
    for row in rows_a:
        result_row = []
        for j in range(n):
            s = 0
            for k in range(n):
                s += row[k] * matrix_b[k][j]
            result_row.append(s)
        result_rows.append(result_row)
    return result_rows

def MAIN(matrix_a, matrix_b):
    n = len(matrix_a)
    max_workers = 4
    # Chia đều các hàng của A cho các process
    chunk_size = (n + max_workers - 1) // max_workers
    batches = [matrix_a[i:i+chunk_size] for i in range(0, n, chunk_size)]

    results = []
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(multiply_rows, batch, matrix_b) for batch in batches]
        for f in futures:
            results.extend(f.result())
    return results