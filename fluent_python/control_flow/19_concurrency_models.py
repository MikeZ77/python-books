import itertools
import time

# 1. Using Threads
from threading import Thread, Event

def spin(msg: str, done: Event) -> None:
    for char in itertools.cycle(r"\|/-"): # All backslashes are left in the string
        status = f"\r{char} {msg}"
        print(status, end="", flush=True)
        if done.wait(.1):
            break
    blanks = " " * len(status)
    print(f"\r{blanks}\r", end="")
        
def slow() -> int:
    time.sleep(3)
    return 42

def supervisor() -> int:
    done = Event()
    spinner = Thread(target=spin, args=("Thinking!", done))
    print(f"spinner object {spinner}") # <Thread(Thread-6 (spin), initial)>
    spinner.start()
    result = slow()
    done.set()
    spinner.join()
    return result

# Event has an internal bool starting False
# Calling set() on it sets it to True
# When False if a thread calls wait() it is blocked until another thread calls set()
# Then wait() returns true

# The basic idea is that we running the loading spinner on a seperate thread (from the main thread)
# until the result is returned.
result = supervisor()
print(result)

# 2. Using Processes
# Threads run concurrently.
# Processes may run in parallel if the OS scheduler decides the processes should run on different CPU cores
# Each Python process has its on GIL (Global Interpreter Lock), meaning that the GIL is not a bottleneck
# The GIL is a lock that controlls object reference counts and internal interpreter state
# Only one thread can hold the lock at any given time

import time
from multiprocessing import Process, Event

# Spin and slow functions remain unchanged
def supervisor():
    done = Event()
    spinner = Process(target=spin, args=("Thinking!", done))
    print(f"spinner object {spinner}") # <Process name='Process-1' parent=19105 initial>
    spinner.start()
    result = slow()
    done.set()
    spinner.join()
    return result

result = supervisor()
print(result)

# As you can see, the multiprocessing library conforms to the Threading API, making them more easily interchangable
# In both cases Event is used to communicate between processes or threads

# 3. Coroutines
# Where threads and processes are driven by OS schedulers, coroutines are driven by an application level event loop
# Everything exists in a single thread
# Manages a queue of pending coroutines and drives them one by one, passing control to another coroutine based
# on an event like I/O happens

import asyncio

# Running in the event loop
async def spin(msg: str) -> None:
    for char in itertools.cycle(r"\|/-"):
        status = f"\r{char} {msg}"
        print(status, flush=True, end='')
        try:
            await asyncio.sleep(.1)
        except asyncio.CancelledError: # raised by cancel()
            break
    blanks = " " * len(status)
    print(f"\r{blanks}\r", end="")

async def slow() -> int:
    await asyncio.sleep(3)
    return 42

async def supervisor() -> int: # Native coroutines are defined with async def
    spinner = asyncio.create_task(spin("Thinking!")) # add the spin function to the event loop
    print(f"spinner object {spinner}") # <Task pending name='Task-2' coro=<spin()
    result = await slow() # Block the execution in supervisor until the slow coroutine returns
    spinner.cancel()
    return result

def main() -> None: 
    result = asyncio.run(supervisor())  # Start the event loop
    print(f'Answer: {result}')


# Note that calling some_coroutine() does not immediatly invoke the function
# It returns a coroutine object that can be scheduled with create_task
main()

# What is we used time.sleep instead of asyncio.sleep ?
# time.sleep would block the main thread, which the event loop runs on.
# spin() never executes, because after three seconds, spinner.cancel() is called.

# asyncio.sleep only blocks that coroutine, allowing other coroutines in the event loop to execute

import math
# A CPU intensive task
def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    
    root = math.isqrt(n)
    for i in range(3, root + 1, 2):
        if n % i == 0:
            return False
    return True

def spin(msg: str, done: Event) -> None:
    for char in itertools.cycle(r"\|/-"): # All backslashes are left in the string
        status = f"\r{char} {msg}"
        print(status, end="", flush=True)
        if done.wait(.1):
            break
    blanks = " " * len(status)
    print(f"\r{blanks}\r", end="")
        
def slow() -> int:
    is_prime(5_000_111_000_222_021)
    return 42

def supervisor_thread() -> int:
    done = Event()
    spinner = Thread(target=spin, args=("Thinking!", done))
    print(f"spinner object {spinner}") # <Thread(Thread-6 (spin), initial)>
    spinner.start()
    result = slow()
    done.set()
    spinner.join()
    return result

def supervisor_process():
    done = Event()
    spinner = Process(target=spin, args=("Thinking!", done))
    print(f"spinner object {spinner}") # <Process name='Process-1' parent=19105 initial>
    spinner.start()
    result = slow()
    done.set()
    spinner.join()
    return result


# Two seperate processes running in parallel, so no issues running a compute intensive task in parallel   
start = time.time()
supervisor_process()
print(time.time() - start)

# Could have issues, because there are two threads competing for the GIL.
# It turns out in this simple example it is not an issue, because spin is interrupted every 5ms allowing is_prime to run
# By default python suspends a thread every 5ms
# Note that spin is not CPU intensive, but if we had multiple CPU intensive tasks/threads, Threading would not perform well.
start = time.time()
supervisor_thread()
print(time.time() - start)

async def spin(msg: str) -> None:
    for char in itertools.cycle(r"\|/-"):
        status = f"\r{char} {msg}"
        print(status, flush=True, end='')
        try:
            await asyncio.sleep(.1)
        except asyncio.CancelledError:
            break
    blanks = " " * len(status)
    print(f"\r{blanks}\r", end="")

async def slow() -> int:
    is_prime(5_000_111_000_222_021)
    return 42

async def supervisor() -> int: 
    spinner = asyncio.create_task(spin("Thinking!")) 
    print(f"spinner object {spinner}")
    result = await slow()
    spinner.cancel()
    return result


# Note that spinner never runs, similar to time.sleep()
# is_prime does not return a coroutine. The await keyword transfers control to slow->is_prime
# and this blocks the main thread.
start = time.time()
asyncio.run(supervisor())  # Start the event loop
print(time.time() - start)

"""
sequential.py: baseline for comparing sequential, multiprocessing,
and threading code for CPU-intensive work.
"""

from time import perf_counter
from typing import NamedTuple

PRIME_FIXTURE = [
    (2, True),
    (142702110479723, True),
    (299593572317531, True),
    (3333333333333301, True),
    (3333333333333333, False),
    (3333335652092209, False),
    (4444444444444423, True),
    (4444444444444444, False),
    (4444444488888889, False),
    (5555553133149889, False),
    (5555555555555503, True),
    (5555555555555555, False),
    (6666666666666666, False),
    (6666666666666719, True),
    (6666667141414921, False),
    (7777777536340681, False),
    (7777777777777753, True),
    (7777777777777777, False),
    (9999999999999917, True),
    (9999999999999999, False),
]

NUMBERS = [n for n, _ in PRIME_FIXTURE]

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    root = math.isqrt(n)
    for i in range(3, root + 1, 2):
        if n % i == 0:
            return False
    return True


class Result(NamedTuple):
    prime: bool
    elapsed: float

def check(n: int) -> Result:
    t0 = perf_counter()
    prime = is_prime(n)
    return Result(prime, perf_counter() - t0)

def main() -> None:
    print(f'Checking {len(NUMBERS)} numbers sequentially:')
    t0 = perf_counter()
    for n in NUMBERS:  # <3>
        prime, elapsed = check(n)
        label = 'P' if prime else ' '
        print(f'{n:16}  {label} {elapsed:9.6f}s')

    elapsed = perf_counter() - t0
    print(f'Total time: {elapsed:.2f}s')

main()

"""
procs.py: shows that multiprocessing on a multicore machine
can be faster than sequential code for CPU-intensive work.
"""

# tag::PRIMES_PROC_TOP[]
import sys
from time import perf_counter
from typing import NamedTuple
from multiprocessing import Process, SimpleQueue, cpu_count
from multiprocessing import queues 

class PrimeResult(NamedTuple): 
    n: int # We need some unique key to keep track of the job, since the results can be stored in any order
    prime: bool
    elapsed: float

JobQueue = queues.SimpleQueue[int]  
ResultQueue = queues.SimpleQueue[PrimeResult] 

def check(n: int) -> PrimeResult: 
    t0 = perf_counter()
    res = is_prime(n)
    return PrimeResult(n, res, perf_counter() - t0)

def worker(jobs: JobQueue, results: ResultQueue) -> None: 
    # Each worker dequeues, works, and stores the result until the queue is empty
    # This works becuase these queues specifically are thread/process safe
    while n := jobs.get(): 
        results.put(check(n))  
    results.put(PrimeResult(0, False, 0.0))  

def start_jobs(
    procs: int, jobs: JobQueue, results: ResultQueue 
) -> None:
    # Put all the job args into the job queue
    for n in NUMBERS: 
        jobs.put(n) 
    # We spawn a process for each processor
    for _ in range(procs):
        # E.g. spawn a process/worker for CPU 1
        proc = Process(target=worker, args=(jobs, results)) 
        proc.start()  
        jobs.put(0) 

def main() -> None:
    if len(sys.argv) < 2: 
        procs = cpu_count() # Get the number of CPUS the system has
    else:
        procs = int(sys.argv[1])

    print(f'Checking {len(NUMBERS)} numbers with {procs} processes:')
    t0 = perf_counter()
    jobs: JobQueue = SimpleQueue()       # Create a queue for storing jobs to be processed
    results: ResultQueue = SimpleQueue() # Create a queue for storing the results of those jobs
    start_jobs(procs, jobs, results)  
    checked = report(procs, results)  
    elapsed = perf_counter() - t0
    print(f'{checked} checks in {elapsed:.2f}s') 
    
def report(procs: int, results: ResultQueue) -> int:
    checked = 0
    procs_done = 0
    while procs_done < procs: 
        n, prime, elapsed = results.get() 
        if n == 0:  
            procs_done += 1
        else:
            checked += 1  
            label = 'P' if prime else ' '
            print(f'{n:16}  {label} {elapsed:9.6f}s')
    return checked

  # When using threads or processes, each thread or process likely outputs a result we need.
  # In order to collect these results, we typically store them in a queue (a common theme in concurrent and distributed computing)
main()

# A race condition: A bug in concurrent programming that may or may not occur depending on the order of events
# For example if A is processed before B, all is fine. But if B is processed before A, then the bug occurs


