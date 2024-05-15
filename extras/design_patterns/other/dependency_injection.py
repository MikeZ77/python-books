# Inversion Control Principle:
#   Software components are desined to recieve a dependencies from an external source ...
#   rather than creating it themselves.

# Benefits:
# 1. Lossely coupled components make changes to the code easier
# 2. Allows for easier testing by passing mocks rather than patching at runtime

# Examples of simple DI

# With a function.
import requests
from typing import Callable

def sends_a_get_request(get: Callable):
    assert isinstance(get, Callable)
    # Here we call get rather than calling in the global scope

if __name__ == "__main__":
    sends_a_get_request(requests.get)
    
    
# With a class
class OurUtilDependency:
    def __init__(self, text: str):
        self.text = text
        
    def parse(self) -> list:
        return self.text.split(" ")

class OurClass:
    def __init__(self, utils: OurUtilDependency):
        # Rather than instantiating our_class here we pass it in.
        self.utils = utils


if __name__ == "__main__":
    utils = OurUtilDependency("Hello World!")
    our_class = OurClass(utils)

# While simple, this makes testing easier ...
# Instead of using monkeypatch.seattr, we can simple pass in the mock needed for the test.

# Also, make the code as modular as possible ...
# For example, if we need to parse a string with Utils before sending a request, this should ...
# be broken into two functions (units).
# Finally, it is a completely valid way of following DI and the inversion control principle.

# Injecting the dependencies using a decorator
import functools

def inject(fn: Callable):
    @functools.wraps(fn)
    def get_request(*args, **kwargs):
        fn(requests.get, *args, **kwargs)
    return get_request

@inject
def sends_a_get_request(get: Callable):
    assert isinstance(get, Callable)

if __name__ == "__main__":
    sends_a_get_request()
    
# But this isn't super useful, because we can't define what we would like to inject.
# With args ...
def inject(**deps):
    def inner(fn: Callable):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            return fn(*deps.values(), *args, **kwargs)
        return wrapper
    return inner

@inject(request=requests.get)
def sends_a_get_request(get: Callable, a: int, b: str):
    assert isinstance(get, Callable)
    assert a == 123 and b == "123"
    
if __name__ == "__main__":
    sends_a_get_request(123, "123")
    
# So we just need to make sure the dependencies get passed in the same order we expect ...
# That being said we could improve this by importing inspect and inspecting the signature ...
# of fn to pass deps in accordingly.

# So how would this look like with testing?

# We would like to mock request.get to return a response we need for one of our test cases:

# Lets redefine sends_a_get_request a bit to make it more useful for the test
@inject(request=requests.get)
def sends_a_get_request(get: Callable):
    return get()


def mock_get_request_return_value():
    return 1

# strip the decorator to get the original function
sends_a_get_request = sends_a_get_request.__wrapped__

def test_sends_a_get_request():
    result = sends_a_get_request(mock_get_request_return_value)
    assert result == 1
    
    
if __name__ == "__main__":
    test_sends_a_get_request()

from functools import partial

# We can do this with classes as well ...
class Inject:
    def __init__(self, *, util):
        self.util = util

    def __call__(self, cls) -> OurClass:
        return partial(cls, self.util) # OurClass
    
@Inject(util=OurUtilDependency("text here")) 
class OurClass:
    def __init__(self, utils: OurUtilDependency):
        self.utils = utils
    

if __name__ == "__main__":
    # NOTE: You can stil use a function decorator here to return the class ...
    # rather than a class decorator.
    our_class = OurClass()

# We can also do this using a metaclass.
# Typically meta class defines how a lass is created, as opposed to how a class is instantiated.

class MockOurUtilDependency:
    ...

class DiMeta(type):
    def __call__(cls, *args, **kwargs):
        if not "utils" in args:
            di_args = (OurUtilDependency("text here"),)
         
        instance = super().__call__(*di_args, **kwargs)
        return instance

# Redefine OurClass to be created from DiMeta
class OurClass(metaclass=DiMeta):
    def __init__(self, utils: OurUtilDependency):
        self.utils = utils
        
if __name__ == "__main__":
    our_class = OurClass()
    our_class = OurClass(MockOurUtilDependency)
    # Could be useful if we have our own classes which are commonly mocked.

# If we are adding more decorators to tasks, stacking many decorators could get confusing
# If there is a decorated which should always be applied (i.e. at the module level) ...
# you can define something like this:

def logger(fn):
    def inner(*args, **kwargs):
        print("Logging:", args, kwargs)
        return fn(*args, **kwargs)
    return inner

@logger
def my_task_1(*args):
    print("my_task_1")

@logger    
def my_task_2(*args):
    print("my_task_2")

@logger  
def my_task_3(*args):
    print("my_task_3")
    
if __name__ == "__main__":
    my_task_1(1, 2, 3)
    my_task_2("a", "b", "c")
    my_task_3([1, 2, 3])
    import sys
    print(sys.modules[__name__]) # Current module object <module '__main__'>
    print(sys.modules[__name__].__dict__) # All the objects bound to this module

from types import ModuleType

def log_module_tasks(module: ModuleType):
    for name, obj in vars(module).items(): # vars -> __dict__
        # Here, check if the object is a callable wrapped in a prefect task
        if name in ["my_task_1", "my_task_2", "my_task_3"]:
            setattr(module, name, logger(obj))
    return module        
    
def my_task_1(*args):
    print("my_task_1")

def my_task_2(*args):
    print("my_task_2")

def my_task_3(*args):
    print("my_task_3")
    
# from common import log_module_tasks
log_module_tasks(sys.modules[__name__])

if __name__ == "__main__":
    my_task_1(1, 2, 3)
    my_task_2("a", "b", "c")
    my_task_3([1, 2, 3])