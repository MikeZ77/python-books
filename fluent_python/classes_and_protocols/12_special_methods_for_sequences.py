# Recall the basic sequence protocol __len__ and __getitem__
# Protocols as an informal interface

from array import array
import reprlib
import math
import operator
import functools

class Vector:
    typecode = "d"
    __match_args__ = ("x", "y", "z", "t")

    def __init__(self, components):
        self._components = array(self.typecode, components)

    def __iter__(self):
        return iter(self._components)
    
    def __repr__(self):
        components = reprlib.repr(self._components) #used to get a limited length
        components = components[components.find("["):-1]
        return f"Vector({components})"

    def __str__(self):
        return str(tuple(self)) # Because we can unpack this using __iter__
    
    def __bytes__(self):
        return (bytes([ord(self.typecode)] + [self._components]))

    def __eq__(self, other):
        # return tuple(self) == tuple(other)

        # More efficient
        # if len(self) != len(other):
        #     return False
        # for a, b in zip(self, other):
        #     if a != b:
        #         return False
        # return True

        # The same in one line
        return len(self) == len(other) and all(a == b for a, b in zip(self, other))

    def __hash__(self):
        hashes = (hash(x) for x in self._components) # We hash/eval each element as neeeded, hence the generator
        return functools.reduce(operator.xor, hashes, 0) # this is map (using hash) and reduce (xor)

    def __abs__(self):
        return math.hypot(*self) # Because of __iter__ I think

    def __bool__(self):
        return bool(abs(self))
    
    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[:1]).cast(typecode)
        return cls(*memv)

    # def __getitem__(self, index):
    #     return self._components[index]

    # But when we slice, we would like to return an instance of its own type (not a list)
    # A slice aware __getitem__
    def __getitem__(self, key):
        if isinstance(key, slice):
            cls = type(self)
            return cls(self._components[key])
        # Passing a single value. Note index(1.2) raises an TypeError, while int(1.2) does not
        index = operator.index(key)
        return self._components[index]
    
    def __getattr__(self, name):
        cls = type(self)
        try:
            pos = cls.__match_args__.index(name)
        except ValueError:
            pos = -1
        if 0 <= pos < len(self._components):
            return self._components[pos]
        msg = f"{cls.__name__!r} object has not attribute {name!r}"
        raise AttributeError(msg)

    def __setattr__(self, name, value):
        cls = type(self)
        if len(name) == 1:
            if name in cls.__match_args__:
                error = "read only attribute {attr_name!r}"
            elif name.islower():
                error = "can't set attributes 'a' to 'z' in {cls_name!r}"
            else:
                error = ""
            if error:
                msg = error.format(cls_name=cls.__name__, attr_name=name)
                raise AttributeError(msg)
        super().__setattr__(name, value) #for any other attribute set it as normal

v1 = Vector(range(5))
print(v1.typecode)
print(v1.__class__.typecode)

v2 = Vector([0.0, 1.1, 2.2, 3.3, 4.4])
# print(v2.a) # Has not attribute a
print(v2.x)
# v2.x = 10.0 # We do not want this  (similar to __var private variable)
print(v2.x)
print(v2)
            
try:
    v2.s = 10.0
except AttributeError as e:
    print(e)
        
v2.apple = 1
print(v2.apple)

# Why do we want to protect a-z as read only, because we want to make Vector hashable
# Takeaway, often when implement __getattr__ you need to implement __setattr__ as well for consistancy
# we add __match_args__ so we can get v2.x instead of v2[0]

# For the hash implementaton creating a tuple could be expensive since we dont know the number of elements
# we can use functools reduce (Needs an operation to reduce an iterable to a single value)
# eg. a0 op a1 = r0, r0 op a2 = r1, ... continue until fully reduced

