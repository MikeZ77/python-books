# Suppose we have three classes, they are only data structures, so it can get repetitive declaring each one.

class Stock:
    def __init__(self, name, shares, price):
        self.name = name
        self.price = price
        self.shares = shares

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Address:
    def __init__(self, host, port):
        self.host = host
        self.port = port


# So basically we would just like to load data into a class dynamically
# One way ...
class Structure:
    _fields = []
    def __init__(self, *args):
        for name, val in zip(self._fields, args): # Access the class variable through the instance
        # for name, val in zip(self.__class__._fields, args):   # same thing
            setattr(self, name, val)

class Stock(Structure):
    _fields = ["name", "price", "shares"]  

class Point(Structure):
    _fields = ["x", "y"]

class Address(Structure):
    _fields = ["host", "port"]


s = Stock("abc", 110, 500)
print(s.name, s.price, s.shares)

# However, a whole bunch of "stuff" you lose from doing it this way.
# No support for keyword args
# No typing
# No function signature
# etc.

from inspect import Parameter, Signature, signature

print(signature(Address)) # (*args) but we want this to be the unique signature for Address init

_fields = ["name", "price", "shares"]
params = [Parameter(fname, Parameter.POSITIONAL_OR_KEYWORD) for fname in _fields]
print(params)

# What can we do with these params? We can bind them to *args and **kwargs
sig = Signature(params)

def foo(*args, **kwargs):
    bound = sig.bind(*args, **kwargs)
    for name, val in bound.arguments.items():
        print(name, val)


foo(1, 2, 3)
foo(1, price=100, shares=200)

# Before we could do Stock("abc", 110) and leave out an arg with no issues
# Now
try:
    foo(1, 2)
except TypeError as exc:
    print(exc)
    
# So we can use this in our Structure to bind params
def make_signature(names):
    return Signature(Parameter(name, Parameter.POSITIONAL_OR_KEYWORD) for name in names)

class Structure:
    __signature__ = make_signature([])
    
    def __init__(self, *args, **kwargs):
        # Do the binding first
        bound = self.__signature__.bind(*args, **kwargs)
        for name, val in bound.arguments.items():
            setattr(self, name, val)
            
class Stock(Structure):
    __signature__ = make_signature(["name", "price", "shares"])

class Point(Structure):
    __signature__ = make_signature(["x", "y"])

class Address(Structure):
    __signature__ = make_signature(["host", "port"])
    
    
print(signature(Stock)) # (name, price, shares)

# Side note: Here is a modern way of doing this using a dataclass
from dataclasses import make_dataclass

Stock = make_dataclass("Stock", [("name", str), ("price", int)])
print(signature(Stock)) # (name: str, price: int) -> None

# As we know dataclasses are mainly used as containers for data, and a lot metadata issues
# are handled automatically, and certain special methods are generated automatically.

# Here is a cleaner way of doing this via a metaclass
class StructureMeta(type):
    def __new__(cls, name, bases, clsdict):
        clsobj = super().__new__(cls, name, bases, clsdict)
        sig = make_signature(clsobj._fields)
        setattr(clsobj, "__signature__", sig)
        return clsobj
    
# So when creating a class using this metaclass we define a behavior that creates a signature from
# the fields class attribute and sets it as the instance class __signature__ attribute like before.

class Structure(metaclass=StructureMeta):
    _fields = []
    def __init__(self, *args, **kwargs):
        bound = self.__signature__.bind(*args, **kwargs)
        for name, val in bound.arguments.items():
            setattr(self, name, val)
            
# So, suppose we have:
class Stock(Structure):
    _fields = ["name", "price", "shares"]

# Class Stock's creation is based off the metaclass StructureMeta
# This modifies the class creation of Stock unlike the normal instance creation
# In this case it takes the _fields attributes and updates the signature on the class which is later used to bind to the args that are passed in.
