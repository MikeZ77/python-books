# operator overloading to support infix operators
from collections import abc
import functools, itertools, operator, reprlib, math
from array import array

class Vector:
    typecode = "d"
    __match_args__ = ("x", "y", "z", "t")

    def __init__(self, components):
        self._components = array(self.typecode, components)

    def __len__(self):
        return len(self._components)
    
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
        return len(self) == len(other) and all(a == b for a, b in zip(self, other))

    def __hash__(self):
        hashes = (hash(x) for x in self._components) # We hash/eval each element as neeeded, hence the generator
        return functools.reduce(operator.xor, hashes, 0) # this is map (using hash) and reduce (xor)

    def __abs__(self):
        return math.hypot(*self) # Because of __iter__ I think

    def __bool__(self):
        return bool(abs(self))
    
    def __add__(self, other):
        pairs = itertools.zip_longest(self, other, fillvalue=0.0)
        return Vector(a + b for a, b in pairs)

    def __radd__(self, other):
        # radd delegates to __add__ for adding different types
        return self + other
    
    def __mul__(self, scalar):
        return Vector(scalar * n for n in self)
    
    def __rmul__(self, scalar):
        return self * scalar
    
    def __matmul__(self, other):
        if isinstance(other, abc.Sized) and isinstance(other, abc.Iterable):
            if len(self) == len(other):
                return sum(a * b for a, b in zip(self, other))
            else:
                raise ValueError("@ requires vectors of equal length")
        else:
            # Python handles NotImplemented by raising a TypeError instead of us doing this check and raising the TypeError ourselfes
            return NotImplemented
            
    def __rmatmul__(self, other):
        return self@other
    
v1 = Vector([1, 2, 3])
v2 = Vector([3, 4, 5])
print(v1 + v2)
print((1, 2, 3) + v2)
print(10 * v1)
try:
    print(10 @ v1)
except TypeError as ex:
    print(ex)

print(v1 @ v2)
