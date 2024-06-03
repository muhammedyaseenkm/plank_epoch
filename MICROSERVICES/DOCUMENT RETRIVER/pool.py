from multiprocessing import Pool, Process, Queue
import time

def f(n):
    sum = 0
    for x in range(1000):
        sum += x * x
    return sum

results = []

def calac_square(numbers, q):
    global results 
    for n in numbers: 
        q.put(n * n)

if __name__ == "__main__":
    t1 = time.time()
    p = Pool()
    result = p.map(f, range(100))
    p.close() 
    p.join()
    
    numbers = range(10000)  
    q = Queue()
    m = Process(target=calac_square, args=(numbers,q))
    m.start()  # Start the process
#    m.join()   # Wait for the process to complete
    
#    while not q.empty(): print(q.get())

    print("pool took time:", time.time() - t1)

import sys
from concurrent.futures import ThreadPoolExecutor

# Increase the limit for integer string conversion
sys.set_int_max_str_digits(1000000000)
with ThreadPoolExecutor(max_workers=5) as executor:
   future = executor.submit(pow, 3200003, 56435)
   print(future.result())
