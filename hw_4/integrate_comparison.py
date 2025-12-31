import math
import time
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def integrate_chunk(args):
    f, a, b, n_iter = args
    acc = 0
    step = (b - a) / n_iter
    for i in range(n_iter):
        acc += f(a + i * step) * step
    return acc

def integrate(f, a, b, *, n_jobs=1, n_iter=10000000, executor_class):
    chunk_iter = n_iter // n_jobs
    step = (b - a) / n_iter
    tasks = []
    
    for i in range(n_jobs):
        iter_count = chunk_iter
        if i == n_jobs - 1:
            iter_count = n_iter - chunk_iter * (n_jobs - 1)
        
        chunk_a = a + (i * chunk_iter) * step
        chunk_b = chunk_a + iter_count * step
        
        tasks.append((f, chunk_a, chunk_b, iter_count))
        
    with executor_class(max_workers=n_jobs) as executor:
        results = executor.map(integrate_chunk, tasks)
        
    return sum(results)

def main():
    cpu_num = multiprocessing.cpu_count()
    n_jobs_list = range(1, cpu_num * 2 + 1)
    
    log = []
    header = f"CPU count: {cpu_num}\nComparison for integrate(math.cos, 0, math.pi/2)"
    log.append(header)
    log.append("n_jobs\tThreadPool\tProcessPool")
    
    print(header)
    print("n_jobs\tThreadPool\tProcessPool")

    N_ITER = 10000000 

    for n_jobs in n_jobs_list:
        # ThreadPoolExecutor
        start = time.time()
        integrate(math.cos, 0, math.pi / 2, n_jobs=n_jobs, n_iter=N_ITER, executor_class=ThreadPoolExecutor)
        time_thread = time.time() - start
        
        # ProcessPoolExecutor
        start = time.time()
        integrate(math.cos, 0, math.pi / 2, n_jobs=n_jobs, n_iter=N_ITER, executor_class=ProcessPoolExecutor)
        time_process = time.time() - start
        
        log_line = f"{n_jobs}\t{time_thread:.4f}\t{time_process:.4f}"
        log.append(log_line)
        print(log_line)
        
    with open("artifacts/4.2.txt", "w") as f:
        f.write("\n".join(log))

if __name__ == "__main__":
    main()

