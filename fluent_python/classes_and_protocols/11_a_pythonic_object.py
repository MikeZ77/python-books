from array import array
import math

class Vector2D:
    typecode = "d"
    __match_args__ = ("x", "y")

    def __init__(self, x, y):
        self.__x = float(x)
        self.__y = float(y)

    @property
    def x(self):
        return self.__x
    
    @property
    def y(self):
        return self.__y

    def __iter__(self):
        return (i for i in (self.x, self.y)) # Makes Vector2D iterable (makes unpacking possible)

    def __repr__(self):
        class_name = type(self).__name__
        return "{}({!r}, {!r})".format(class_name, *self)

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):
        return (bytes(ord(self.typecode))) + bytes(array(self.typecode, self))

    def __eq__(self, other):
        return tuple(self) == tuple(other) # can convert to tuple becuase __iter__

    def __abs__(self):
        return math.hypot(self.x, self.y)
    
    def __bool__(self):
        return bool(abs(self))
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[:1]).cast(typecode)
        return cls(*memv)
    
    # @classmethod changes the way the class is called, so recieved the class as the first arg
    # Its most common use is for an alternative constructor, like in this case returning the instance from bytes
    # @staticmethod on the other hand is just a plain function
    # @staticmethod doesnt really have a good use case, since it a function that does the same thing can still be placed nearby the class

v1 = Vector2D(1, 2)
# To make vector hashable, we need to implement __hash__ (__eq__ is also required which we already have)
# So the vector instance needs to be immutable
# Use __ to make the attribute private
# This way we cannot v1.x = 10
# We add @property so the attributes can still be accessed (like a getter)
# Now we can implement hash. Hash will use the __eq__ method to compare

print(hash(v1))

# We can also do pattern matching
# Note: this could be very useful for directions
def keyword_pattern_demo(v: Vector2D) -> None:
    match v:
        case Vector2D(x=0, y=0):
            print(f"{v!r} not moving")
        case Vector2D(x=1, y=0):
            print(f"{v!r} moving right")
        case Vector2D(x=-1, y=0):
            print(f"{v!r} moving left")

keyword_pattern_demo(Vector2D(1, 0))
# To make pattern matching work woth positional args we neeed to add __match_args__
def keyword_pattern_demo(v: Vector2D) -> None:
    match v:
        case Vector2D(0, 0):
            print(f"{v!r} not moving")
        case Vector2D(1, 0):
            print(f"{v!r} moving right")
        case Vector2D(-1, 0):
            print(f"{v!r} moving left")

keyword_pattern_demo(Vector2D(1, 0))

# Private and protected attributes in python
# using two leading unserscores makes the attribute private
# This is also known as mangling since for example __mood becomes _Dog__mood and _Beagle__mood
# Basically its main purpose is to stop you from overriding the variable without knowing it

# You can also use a single leading quote. Nothing is enforced but it is a very strong convention 
# Just like ALL_CAPS is for constants
# Some call single leading quote protected

# Saving memory with slots
# Python stores the attributes of instances in a dict named __dict__
# This can use more memory, an alternative is __slots__

class Pixel:
    __slots__ = ("x", "y")

p = Pixel()
try:
    print(p.__dict__)
except AttributeError as e:
    print(e)

p.x = 1
p.y = 2

try:
    p.color = "red"
except AttributeError as e:
    print(e)

# http://tech.oyster.com/save-ram-with-python-slots/
# Dont prematurely optimize. 
# This is normally only useful if you have a huge number of objects

# Overriding class attributes
class ParentClass: thing = 12
c = ParentClass()
print(c.thing)
c.thing = 1
print(c.thing) # But this does not change the class attribute
d = ParentClass()
print(d.thing)
# The most common way is to subclass just for the class attribute
class ChildClass(ParentClass): thing = 1
e = ChildClass()
print(e.thing)


