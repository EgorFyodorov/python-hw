import time
import threading
import multiprocessing
import os

def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)

def run_synchronous(n, count):
    start = time.time()
    for _ in range(count):
        fib(n)
    end = time.time()
    return end - start

def run_threading(n, count):
    threads = []
    start = time.time()
    for _ in range(count):
        t = threading.Thread(target=fib, args=(n,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    end = time.time()
    return end - start

def run_multiprocessing(n, count):
    processes = []
    start = time.time()
    for _ in range(count):
        p = multiprocessing.Process(target=fib, args=(n,))
        processes.append(p)
        p.start()
        
    for p in processes:
        p.join()
    end = time.time()
    return end - start

def main():
    N = 32
    COUNT = 10
    
    print(f"Running Fibonacci({N}) x {COUNT} times...")
    
    time_sync = run_synchronous(N, COUNT)
    print(f"Synchronous: {time_sync:.4f}s")
    
    time_threads = run_threading(N, COUNT)
    print(f"Threading: {time_threads:.4f}s")
    
    time_processes = run_multiprocessing(N, COUNT)
    print(f"Multiprocessing: {time_processes:.4f}s")
    
    output = (
        f"Fibonacci({N}) calculation {COUNT} times:\n"
        f"Synchronous: {time_sync:.4f}s\n"
        f"Threading: {time_threads:.4f}s\n"
        f"Multiprocessing: {time_processes:.4f}s\n"
    )
    
    with open("artifacts/4.1.txt", "w") as f:
        f.write(output)

if __name__ == "__main__":
    main()
