from concurrent.futures import ProcessPoolExecutor
import multiprocessing as mp

def calc_fib_batch(batch, mod):
    output = []
    for val in batch:
        a, b = 0, 1
        # Dùng fast doubling dựa trên bit của val
        for bit in bin(val)[2:]:
            temp1 = (a * ((2 * b - a) % mod)) % mod
            temp2 = (a * a + b * b) % mod
            if bit == '1':
                a, b = temp2, (temp1 + temp2) % mod
            else:
                a, b = temp1, temp2
        output.append(a)
    return output

def MAIN(input_filename="input.txt"):
    with open(input_filename) as f:
        items = list(map(int, f.read().split()))
    if not items:
        return []
    N = items[0]
    Q = items[1]
    arr = items[2:2+N]
    values = [x + 1 for x in arr]  # F(0)=1, F(1)=1, ... nên cần +1
    # Chia batch nhỏ hơn một chút cho load đều CPU
    n_proc = mp.cpu_count()
    chunk = max(5000, len(values)//(n_proc*2))
    batches = [values[i:i+chunk] for i in range(0, len(values), chunk)]
    result = []
    with ProcessPoolExecutor(max_workers=n_proc) as executor:
        tasks = [executor.submit(calc_fib_batch, b, Q) for b in batches]
        for t in tasks:
            result.extend(t.result())
    return result

if __name__ == '__main__':
    mp.set_start_method('fork', force=True)
    MAIN("input.txt")