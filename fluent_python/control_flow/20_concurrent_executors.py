#!/usr/bin/env python3

"""Download flags of top 20 countries by population

Sequential version

Sample runs (first with new domain, so no caching ever)::

    $ ./flags.py
    BD BR CD CN DE EG ET FR ID IN IR JP MX NG PH PK RU TR US VN
    20 downloads in 26.21s
    $ ./flags.py
    BD BR CD CN DE EG ET FR ID IN IR JP MX NG PH PK RU TR US VN
    20 downloads in 14.57s


"""

# tag::FLAGS_PY[]
import time
from pathlib import Path
from typing import Callable

import httpx  # <1>

POP20_CC = ('CN IN US ID BR PK NG BD RU JP '
            'MX PH VN ET EG DE IR TR CD FR').split()  # <2>

BASE_URL = 'https://www.fluentpython.com/data/flags'  # <3>
DEST_DIR = Path('downloaded')                         # <4>

def save_flag(img: bytes, filename: str) -> None:     # <5>
    (DEST_DIR / filename).write_bytes(img)

def get_flag(cc: str) -> bytes:  # <6>
    url = f'{BASE_URL}/{cc}/{cc}.gif'.lower()
    resp = httpx.get(url, timeout=6.1,       # <7>
                     follow_redirects=True)  # <8>
    resp.raise_for_status()  # <9>
    return resp.content

def download_many(cc_list: list[str]) -> int:  # <10>
    for cc in sorted(cc_list):                 # <11>
        image = get_flag(cc)
        save_flag(image, f'{cc}.gif')
        print(cc, end=' ', flush=True)         # <12>
    return len(cc_list)

def main(downloader: Callable[[list[str]], int]) -> None:  # <13>
    DEST_DIR.mkdir(exist_ok=True)                          # <14>
    t0 = time.perf_counter()                               # <15>
    count = downloader(POP20_CC)
    elapsed = time.perf_counter() - t0
    print(f'\n{count} downloads in {elapsed:.2f}s')

if __name__ == '__main__':
    main(download_many)     # <16>
# end::FLAGS_PY[]

# Download using threads using concurrent.futures executor
from concurrent import futures

# cc => country code
def download_one(cc: str):
    image = get_flag(cc)
    save_flag(image, f"{cc}.gif")
    print(cc, end=" ", flush=True)
    return cc

def download_many(cc_list: list[str]) -> int:
    with futures.ThreadPoolExecutor() as executor:
        res = executor.map(download_one, sorted(cc_list))
    return len(list(res))

main(download_many)

# Note the refactoring that occured: In the sequential example download_one is the block of the for loop in download_many
# We refactor this s.t. this body is called concurrently

# How does Future work behind the scenes?
# A Future object represents a deffered computation that may or may not succeed (like a Promise in js)
# We don't interact with the Future object directly, it is something that is scheduled to run by the framework
# Both asyncio and concurrent.futures use a Future object

# The executor.map method is calling submit (takes a callable, schedules it to run, and returns a Future)
# An example using submit() without map

def download_many(cc_list: list[str]) -> int:
    cc_list = cc_list[:5]
    with futures.ThreadPoolExecutor(max_workers=3) as executor:
        to_do: list[futures.Future] = []
        for cc in sorted(cc_list):
            future = executor.submit(download_one, cc)
            to_do.append(future)
            print(f"Scheduled for {cc}: {future}")

        for count, future in enumerate(futures.as_completed(to_do), 1): # as_completed yields Futures as they are completed 
            res: str = future.result() # gets the result from the future (does not block)
            print(f"{future} result: {res!r}")
            
        return count
    
main(download_many)

# Launching processes with concurrent.futures

# concurrent.futures allows us to easily switch to a process based solution to get around issues with the GIL and because their interfaces are so similar
def download_many(cc_list: list[str]) -> int:
    cc_list = cc_list[:5]
    with futures.ProcessPoolExecutor() as executor: # By default max_workers is your CPU core count
        to_do: list[futures.Future] = []
        for cc in sorted(cc_list):
            future = executor.submit(download_one, cc)
            to_do.append(future)
            print(f"Scheduled for {cc}: {future}")

        for count, future in enumerate(futures.as_completed(to_do), 1):
            res: str = future.result()
            print(f"{future} result: {res!r}")
            
        return count
    
main(download_many)

# There is no advantage to using processes for this example, and infact there is more overhead.
# If this example did more processing/computation instead of network calls, then using processes would make sense.

# Now lets take a look at how we can simplify the code for the prime checker using concurrent.futures:
import sys
import math
from typing import NamedTuple
from time import perf_counter
############################################# This code is the same as before #############################################
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
###################################################################################################################
class PrimeResult(NamedTuple):
    n: int
    flag: bool
    elapsed: float

def check(n: int) -> PrimeResult:
    t0 = perf_counter()
    res = is_prime(n)
    return PrimeResult(n, res, perf_counter() - t0)

def main() -> None:
    if len(sys.argv) < 2:
        workers = None
    else:
        workers = int(sys.argv[1])
    
    executor = futures.ProcessPoolExecutor(workers)
    actual_workers = executor._max_workers
    
    print(f"Checking {len(NUMBERS)} numbers with {actual_workers} processes:")

    t0 = perf_counter()
    numbers = sorted(NUMBERS, reverse=True)
    with executor:
        for n, prime, elapsed in executor.map(check, NUMBERS):
            label = "p" if prime else ""
            print(f"{n:16} {label} {elapsed:9.6f}s")
    
    time = perf_counter() - t0
    print(f"Total time: {time:.2f}s")
    
    
main()

# Experimenting with executor.map
# What happens using the ThreadPoolExecutor when you run it with 3 threads and 5 callables?

from time import sleep, strftime
from concurrent import futures

def display(*args):  # <1>
    print(strftime('[%H:%M:%S]'), end=' ')
    print(*args)

def loiter(n):  # <2>
    msg = '{}loiter({}): doing nothing for {}s...'
    display(msg.format('\t'*n, n, n))
    sleep(n)
    msg = '{}loiter({}): done.'
    display(msg.format('\t'*n, n))
    return n * 10  # <3>

def main():
    display('Script starting.')
    executor = futures.ThreadPoolExecutor(max_workers=3)  # <4>
    results = executor.map(loiter, range(5))  # <5>
    display('results:', results)  # <6>
    display('Waiting for individual results:')
    for i, result in enumerate(results):  # <7>
        display(f'result {i}: {result}')

main()

# The limitation with map here is that we do not get the results back as they are ready.
# say thread 0 finishes first, then it is ready to pick up the third item
# we don't get that result right away, we need to wait for all to complete
# This wouldnt be as much of an issue had we selected max_workers=5



