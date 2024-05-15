def deco(func):
    def inner():
        print("Running inner")
    return inner

inner = deco(lambda x: print(x)) # We can call a decorator like a regular func
inner()

@deco
def target():
    print("runhning target()")

target()

registry = []

def register(func):
    print(f"runnign register {func}")
    registry.append(func)
    return func

@register
def f1():
    print("running f1()")

@register
def f2():
    print("running f2()")

@register
def f3():
    print("running f3()")

# This code is not useless, think about mapping url patterns to functions that generate an HTTP response
def make_average():
    series = [] # free variable
    def averager(new_value):
        series.append(new_value)
        return sum(series) / len(series)
    return averager

averager = make_average()
print(averager(1))
print(averager(2))
print(averager(3))

# here series variable is bound to averager
# it can be used when the function is invoked even though its defining scope (make_average) is not available

# def make_averager():
#     count = 0
#     total = 0
#     def averager(new_value):
#         count += 1
#         total += new_value
#         return total / count
#     return averager

# The problem here is that count += 1 => count = count + 1 which is assignment. That makes count and total local to averager. 
# Error referenced before assignment

def make_averager():
    count = 0
    total = 0
    def averager(new_value):
        nonlocal count, total
        count += 1
        total += new_value
        return total / count
    return averager

averager = make_average()
print(averager(1))
print(averager(2))
print(averager(3))

import time

# Simple decorator example
def clock(func):
    def clocked(*args):
        t0 = time.perf_counter()
        result = func(*args)
        elapsed = time.perf_counter() - t0
        name = func.__name__
        arg_str = ", ".join(repr(arg) for arg in args)
        print(f"[{elapsed:0.8f}s {name}({arg_str}) -> {result!r}]")
        return result
    return clocked

# Shortcomings does no accept kwargs and masks the __name__ and __doc__ of the decorated function

@clock
def factorial(n):
    """Does factorial """
    return 1 if n <= 1 else n * factorial(n-1)

print(factorial(100))
print(factorial.__name__) # clocked
print(factorial.__doc__) # None

import functools

def clock(func):
    @functools.wraps(func)
    def clocked(*args, **kwargs):
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - t0
        name = func.__name__
        arg_str = ", ".join(repr(arg) for arg in args)
        kwarg_str = ", ".join(f"{kwarg=}" for kwarg in kwargs)
        print(f"[{elapsed:0.8f}s {name}({arg_str},{kwarg_str}) -> {result!r}]")
        return result
    return clocked

@clock
def factorial(n):
    """Does factorial """
    return 1 if n <= 1 else n * factorial(n-1)

print(factorial.__name__) # clocked
print(factorial.__doc__) # None

# Decorators in the standard library
# Memoization => saving results of previous expensive operations

def fib(n):
    if n < 2:
        return n
    return fib(n-2) + fib(n-1)

t0 = time.perf_counter()
fib(10)
print(time.perf_counter() - t0)

import functools

@functools.cache
def fib(n):
    if n < 2:
        return n
    return fib(n-2) + fib(n-1)

t0 = time.perf_counter()
fib(10)
print(time.perf_counter() - t0)

# Stacked decorators
"""
@alpha
@beta
@thea
def my_func():
    print("func")

# Behaves like alpha(beta(theta(func)))    
"""

# Note that for functools.cache, the parameters must be hashable, because these are used as the keys
# A more useful case for functools.cache => fetching information from remote API's
# Note that lru_cache adds more functionality

# @lru_cache(maxsize=2**20)
# def costly_func(a, b):

# In other languages we can overload functions with different arguments
from functools import singledispatch
from collections import abc
import fractions
import decimal
import html
import numbers

@singledispatch
def htmlize(obj: object) -> str:
    content = html.escape(repr(obj))
    return f"<pre>{content}</pre>"

@htmlize.register
def _(text: str) -> str:
    content = html.escape(text).replace("\n", "<br/>\n")
    return f"<p>{content}</p>"

@htmlize.register
def _(seq: abc.Sequence) -> str:
    inner = "</li>\n<li>".join(htmlize(item) for item in seq)
    return "<ul>\n<li>" + inner + "</li>\n</ul>"

@htmlize.register
def _(seq: abc.Sequence, num: int) -> str:
    inner = "</li>\n<li>".join(htmlize(item) for item in seq)
    return "<ul>\n<li>" + inner + "</li>\n</ul>" + num

# it also lets us register functions from different modules
# Parameterized decorators
# In order to use params, need to create a decorator factory
registry = set()

def register(active=True):
    def decorate(func):
        print(f"frunning register {active=} -> decorator {func.__name__}")
        if active:
            registry.add(func)
        else:
            registry.discard(func)
        return func
    return decorate


@register(active=True)
def f1():
    print("f1")

# basically, register is the decorator factory
# decorate is the actual decorator function
# register imediately returns the decorated function, but leaves the params as free variables

