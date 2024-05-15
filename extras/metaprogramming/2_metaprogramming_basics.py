# Decorators

def debug(func):
    def wrapper(*args, **kwargs):
        print(func.__name__)
        return func(*args, **kwargs)
    return wrapper

@debug
def adder(x, y):
    """This function does addition"""
    print(x + y)
   
# debug(adder) 
adder(1, 2)

print(adder.__name__) # wrapper
print(adder.__doc__) # None

from functools import wraps

def debug(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(func.__name__)
        return func(*args, **kwargs)
    return wrapper

@debug
def adder(x, y):
    """This function does addition"""
    print(x + y)

print(adder.__name__) # adder
print(adder.__doc__) # This function does addition

# Decorators with arguments
def debug(prefix=""):
    def decorate(func):
        msg = prefix + func.__name__
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(msg)
            return func(*args, **kwargs)
        return wrapper
    return decorate

@debug(prefix="***")
def adder(x, y):
    """This function does addition"""
    print(x + y)

adder(1, 2)

from functools import partial

# However, we can also do this trick
def debug(func=None, *, prefix=""):
    if func is None:
        # The idea here is that if debug was called without func, return a callable
        return partial(debug, prefix=prefix)
        
    msg = prefix + func.__name__
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(msg)
        return func(*args, **kwargs)
    return wrapper

@debug(prefix="***")
def adder(x, y):
    """This function does addition"""
    print(x + y)

adder(1, 2)

# What happens
# debug(prefix="***") debug gets called with prefix
# partial(debug, prefix=prefix) returns the callable partially applied debug function 
# debug(partial(debug, prefix=prefix)) this gets passed as func as normal


# Adding a decorator to a class
def debug_methods(cls):
    for key, val in vars(cls).items(): # same as __dict__
        if callable(val):
            setattr(cls, key, debug(val)) 
    
    return cls

# What this does, get all the attributes of the class
# If it is a method, then replace it dynamically with the decorate version

@debug_methods
class Stuff:
    def add_stuff(self, x, y):
        print(x + y)

    def subtract_stuff(self, x, y):
        print(x - y)

    def multiply_stuff(self, x, y):
        print(x * y)


s = Stuff()
s.add_stuff(1, 2)
s.subtract_stuff(1, 2)
s.multiply_stuff(1, 2)

# A class decorator
from functools import update_wrapper

class cached:
    def __init__(self, func):
        self.func = func
        self.cached_data = {}
        update_wrapper(self, func)

    def __call__(self, *args):
        try:
            return self.cached_data[args]
        except KeyError:
            self.cached_data[args] = ret = self.func(*args)
            return ret


@cached
def exp(x: int) -> int:
    return x ** x

# cached(exp) is how __call__ is used
exp(2)
exp(2)
exp(3)