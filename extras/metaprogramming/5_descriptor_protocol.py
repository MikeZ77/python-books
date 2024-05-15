# Suppose we have a class and want to do some type checking on its properties

class Stock:
    def __init__(self, price, name, shares):
        self._price = price
        self._name = name
        self._shares = shares

    @property
    def shares(self):
        return self._shares
    
    @shares.setter
    def shares(self, value):
        if not isinstance(value, int):
            raise TypeError("expected int")
        if value < 0:
            raise ValueError("must have positive shares")
        self._shares = value
        
s = Stock(8, "abc", 500)
print(s.shares)
s.shares += 100
print(s.shares)

# The problem is that structuring it like this gets very verbose and time consuming 
# Also we have mixed in different checks along with the type checking

# A better way ...
# Note that properties are implemented via "descriptors"
# __get__, __set__, __delete__ etc.
# Are customized processing of attribute access

class Descriptor:
    """Captures get, set and delete attributes"""
    def __init__(self, name=None):
        self.name = name            

    def __get__(self, instance, cls):
        # print("Get", self.name)
        # print(self, instance) # <__main__.Descriptor object at 0x7fce9c463610> <__main__.Stock object at 0x7fce9c463730>
        if instance is None:
            return self
        else:
            return instance.__dict__[self.name]
        
    def __set__(self, instance, value):
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]

class Stock:
    name = Descriptor("name")
    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

s = Stock("GOOG", 100, 200)
s.name 
del s.name
# The idea is that we intercept the dot operator, and do something.

# Creating a type checker
class Descriptor:
    """Captures get, set and delete attributes"""
    def __init__(self, name=None):
        self.name = name            
        
    def __set__(self, instance, value):
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]

class Typed(Descriptor):
    ty = object # expected type
    def __set__(self, instance, value):
        if not isinstance(value, self.ty):
            raise TypeError(f"Expected {self.ty}")
        super().__set__(instance, value)
        
class Integer(Typed):
    ty = int
    
class Float(Typed):
    ty = float

class String(Typed):
    ty = str

from inspect import Parameter, Signature

_fields = ["name", "price", "shares"]
params = [Parameter(fname, Parameter.POSITIONAL_OR_KEYWORD) for fname in _fields]

def make_signature(names):
    return Signature(Parameter(name, Parameter.POSITIONAL_OR_KEYWORD) for name in names)

class StructureMeta(type):
    def __new__(cls, name, bases, clsdict):
        clsobj = super().__new__(cls, name, bases, clsdict)
        sig = make_signature(clsobj._fields)
        setattr(clsobj, "__signature__", sig)
        return clsobj
    
class Structure(metaclass=StructureMeta):
    _fields = []
    def __init__(self, *args, **kwargs):
        bound = self.__signature__.bind(*args, **kwargs)
        for name, val in bound.arguments.items():
            setattr(self, name, val)
            
class Stock(Structure):
    _fields = ["name", "shares", "price"]
    name = String("name")
    shares = Integer("shares")
    price = Float("price")
    
s = Stock("abc", 110, 500.11)

# We can also do mixin classes
class Positive:
    def __set__(self, instance, value):
        if value < 0:
            print(value)
            raise ValueError(f"{value} is not greater than zero")
        super().__set__(instance, value)
      
            

class PositiveInteger(Positive, Integer): ...

class Stock(Structure):
    _fields = ["name", "shares", "price"]
    name = String("name")
    shares = PositiveInteger("shares")
    price = Float("price")

try:
    s = Stock("abc", -110, 500.11)
except ValueError as exc:
    print(exc)