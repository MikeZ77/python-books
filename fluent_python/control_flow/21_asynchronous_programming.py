"""
The two main async methods covered here:

Native coroutines: 
Is a couroutine function defined with async def. You delegate from a coroutine to another coroutine using
the await keyword. Native couroutines have taken over from classic coroutines which are not covered.

Asyncronous generators:
A generator defined with async def and uses the yield keyword in its body (makes it a generator).
Returns an async generator object that implements __anext__ (a coururine method to retrieve the next
item).
"""

# A simple example of probing domains async
import asyncio
import socket
from keyword import kwlist

MAX_KEYWORD_LEN = 4


async def probe(domain: str) -> tuple[str, bool]:
    loop = asyncio.get_running_loop() # returns the asyncio event loop
    try:
        await loop.getaddrinfo(domain, None) # the asyncio event loop comes with this method. It is a coroutine so we await its result.
        # But we could have any coroutine here depending on our use case
        # note that await => yield control to the event loop (and return the result).
    except socket.gaierror:
        return (domain, False)
    return (domain, True)


async def main() -> None:
    names = (kw for kw in kwlist if len(kw) <= MAX_KEYWORD_LEN) # A generator expression since kwlist could be large
    domains = (f'{name}.dev'.lower() for name in names)
    coros = [probe(domain) for domain in domains] # The list of corutines we need to run.
    for coro in asyncio.as_completed(coros): # Waits for the yielded coroutine to resolve. Returned in the order completed not submitted.
        domain, found = await coro # We know from asyncio.as_completed coro is resolved. But we still need await to get the data. It is non-blocking because the coro is resolved.
        mark = '+' if found else ' '
        print(f'{mark} {domain}')


if __name__ == '__main__':
    # asyncio.run starts the event loop and returns only when the event loop exits.
    # This is a common pattern, implement a main coroutine (that calls other coroutines) and drive it with asyncio.run.
    asyncio.run(main())


"""
Concept:

Just like the for keyword works with Iterables, the await keyword works with awaitables.
An awaitable is a:
    - native coroutine object (async def)
    - an asyncio.Task() which you get by passing a native coroutine to asyncio.create_task()
"""
# So getaddrinfo returns a native Courutine. Lets create a task and addd it to the event loop in a similar way.

import random
random.seed(10) # So we can tell that the Tasks are actually finising in a different order


async def modify_int(i):
    return i + 2


async def add_to_event_loop(i):
    loop = asyncio.get_event_loop()
    return await loop.create_task(modify_int(i)) # Notice here we are awaiting a Task rather than a coroutine
    
    
async def gets_stuff():
    l = [random.randint(-i, i) for i in range(10)]
    coros = [add_to_event_loop(i) for i in l]
    for coro in asyncio.as_completed(coros):
        i = await coro
        print(i)
    
    
if __name__ == '__main__':
    asyncio.run(gets_stuff())

# Downloading with asyncio and httpx

from typing import Callable
from pathlib import Path
from httpx import AsyncClient
import time

BASE_URL = 'https://www.fluentpython.com/data/flags'
DEST_DIR = Path('downloaded')  
POP20_CC = ('CN IN US ID BR PK NG BD RU JP '
            'MX PH VN ET EG DE IR TR CD FR').split()

def save_flag(img: bytes, filename: str) -> None:    
    (DEST_DIR / filename).write_bytes(img)

async def get_flag(client: AsyncClient, cc: str) -> bytes:
    url = f"{BASE_URL}/{cc}/{cc}.gif"
    resp = await client.get(url, timeout=6.1, follow_redirects=True)
    return resp.read()

async def download_one(client: AsyncClient, cc: str):
    image = await get_flag(client, cc)
    save_flag(image, f"{cc}.gif")
    print(cc, end=" ", flush=True)
    return cc

async def supervisor(cc_list: list[str]) -> int:
    async with AsyncClient() as client:
        to_do = [download_one(client, cc) for cc in cc_list]
        res = await asyncio.gather(*to_do)
    return len(res)    
    
def download_many(cc_list: list[str]) -> int:
    return asyncio.run(supervisor(cc_list))
          
def main(downloader: Callable[[list[str]], int]) -> None:  # <13>
    DEST_DIR.mkdir(exist_ok=True)                          # <14>
    t0 = time.perf_counter()                               # <15>
    count = downloader(POP20_CC)
    elapsed = time.perf_counter() - t0
    print(f'\n{count} downloads in {elapsed:.2f}s')

if __name__ == '__main__':
    main(download_many)

# gather vs as_completed
# gather takes a list of coroutines and schedules them automatically in the event loop. Once ALL are complete it returns the results for each in a same ordered list
# as_completed again takes a list of coroutines and returns a generator, yielding the result as it finishes. 
# Unlike gather you must get a reference to the event loop and add the couroutine/task yourself.

# Here is an example of a hypothetical async context manager
# Think of use caseses where you have to make a connection to a database on enter and rollback or commit the transaction on exit

async def log(message):
    print(message)

class Example:
    async def __aenter__(self):
        await log('entering context')
        return self
        
    async def __aexit__(self, exc_type, exc, tb):
        await log('exiting context')
        return True

async def example():
    async with Example() as e:
        print(e)
        raise Exception("This exception will be suppressed")


if __name__ == '__main__':
    asyncio.run(example())
        

# Recall that with asyncio.gather we wait for all the coroutines to finish
# This blocks the entire event loop
# what if we needed to provide updates (get results) as each item completes? use asyncio.as_completed like before.
# This example also uses a semaphore for rate limiting
"""
lock -> only allows one thread to enter and is not shared by any proccesses
mutex -> same as a lock but is system wide (sahred between processes)
semaphore -> allows x number of threads to enter

Note that is is all for controlling shared resources.

I guess in this case asyncio.Semaphore is for limiting coroutines from accessing a resource for some event loop.
Note that the event loop lives on a single thread

"""

# NOTE: No point in trying to run this ... too much code. Just added it here for the concept.

# import asyncio
# from collections import Counter
# from http import HTTPStatus
# from pathlib import Path
# from enum import Enum

# import httpx
# import tqdm  # type: ignore

# DownloadStatus = Enum('DownloadStatus', 'OK NOT_FOUND ERROR')

# # low concurrency default to avoid errors from remote site,
# # such as 503 - Service Temporarily Unavailable
# DEFAULT_CONCUR_REQ = 5
# MAX_CONCUR_REQ = 1000

# async def get_flag(client: httpx.AsyncClient,  # <1>
#                    base_url: str,
#                    cc: str) -> bytes:
#     url = f'{base_url}/{cc}/{cc}.gif'.lower()
#     resp = await client.get(url, timeout=3.1, follow_redirects=True)   # <2>
#     resp.raise_for_status()
#     return resp.content

# async def download_one(client: httpx.AsyncClient,
#                        cc: str,
#                        base_url: str,
#                        semaphore: asyncio.Semaphore,
#                        verbose: bool) -> DownloadStatus:
#     try:
#         async with semaphore:  # <3>
#             image = await get_flag(client, base_url, cc)
#     except httpx.HTTPStatusError as exc:  # <4>
#         res = exc.response
#         if res.status_code == HTTPStatus.NOT_FOUND:
#             status = DownloadStatus.NOT_FOUND
#             msg = f'not found: {res.url}'
#         else:
#             raise
#     else:
#         await asyncio.to_thread(save_flag, image, f'{cc}.gif')  # <5>
#         status = DownloadStatus.OK
#         msg = 'OK'
#     if verbose and msg:
#         print(cc, msg)
#     return status
# # end::FLAGS2_ASYNCIO_TOP[]

# # tag::FLAGS2_ASYNCIO_START[]
# async def supervisor(cc_list: list[str],
#                      base_url: str,
#                      verbose: bool,
#                      concur_req: int) -> Counter[DownloadStatus]:  # <1>
#     counter: Counter[DownloadStatus] = Counter()
#     semaphore = asyncio.Semaphore(concur_req)  # <2>
#     async with httpx.AsyncClient() as client:
#         to_do = [download_one(client, cc, base_url, semaphore, verbose)
#                  for cc in sorted(cc_list)]  # <3>
#         to_do_iter = asyncio.as_completed(to_do)  # <4>
#         if not verbose:
#             to_do_iter = tqdm.tqdm(to_do_iter, total=len(cc_list))  # <5>
#         error: httpx.HTTPError | None = None  # <6>
#         for coro in to_do_iter:  # <7>
#             try:
#                 status = await coro  # <8>
#             except httpx.HTTPStatusError as exc:
#                 error_msg = 'HTTP error {resp.status_code} - {resp.reason_phrase}'
#                 error_msg = error_msg.format(resp=exc.response)
#                 error = exc  # <9>
#             except httpx.RequestError as exc:
#                 error_msg = f'{exc} {type(exc)}'.strip()
#                 error = exc  # <10>
#             except KeyboardInterrupt:
#                 break

#             if error:
#                 status = DownloadStatus.ERROR  # <11>
#                 if verbose:
#                     url = str(error.request.url)  # <12>
#                     cc = Path(url).stem.upper()   # <13>
#                     print(f'{cc} error: {error_msg}')
#             counter[status] += 1

#     return counter

# def download_many(cc_list: list[str],
#                   base_url: str,
#                   verbose: bool,
#                   concur_req: int) -> Counter[DownloadStatus]:
#     coro = supervisor(cc_list, base_url, verbose, concur_req)
#     counts = asyncio.run(coro)  # <14>

#     return counts

# if __name__ == '__main__':
#     main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)

# One disadvantage of python is that there is no async file io.
# File io will block the mean thread and also the event loop.
# So, if you need to do file io inside the event loop, you can use 
# await asyncio.to_thread(save_flag, image, f'{cc}.gif') from the above example.

# async generator

import sys
import asyncio
import socket
from collections.abc import Iterable, AsyncIterator
from typing import NamedTuple, Optional

class Result(NamedTuple):
    domain: str
    found: bool

OptionalLoop = Optional[asyncio.AbstractEventLoop]

async def probe(domain: str, loop: OptionalLoop = None) -> Result:
    if loop is None:
        loop = asyncio.get_running_loop()
    try:
        await loop.getaddrinfo(domain, None)
    except socket.gaierror:
        return Result(domain, False)
    return Result(domain, True)

async def multi_probe(domains: Iterable[str]) -> AsyncIterator[Result]: # AsyncGenerator ?
    loop = asyncio.get_running_loop()
    coros = [probe(domain, loop) for domain in domains]
    for coro in asyncio.as_completed(coros):
        result = await coro
        yield result # This makes multi_probe an async generator


async def main(tld: str) -> None:
    tld = tld.strip('.')
    names = (kw for kw in kwlist if len(kw) <= 4)  # <1>
    domains = (f'{name}.{tld}'.lower() for name in names)  # <2>
    print('FOUND\t\tNOT FOUND')  # <3>
    print('=====\t\t=========')
    async for domain, found in multi_probe(domains):  # we use use async for because multi_probe is a coroutine. 
        indent = '' if found else '\t\t'  # <5>       # Note that async for still runs sync based on what it is given  
        print(f'{indent}{domain}')


if __name__ == '__main__':
    # if len(sys.argv) == 2:
    asyncio.run(main("COM"))  # <6>
    # else:
    #     print('Please provide a TLD.', f'Example: {sys.argv[0]} COM.BR')
    
    
# We could also write something similar using a generator expression ...

# async def get_valid_domain_names():
#     names = "python.org rust-lang.org golang.org no-lang.invalid".split()
#     gen_found = (name async for name, found in multi_probe(names) if found)
#     async for name in gen_found:
#         print(name)

