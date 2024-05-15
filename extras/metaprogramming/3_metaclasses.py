# Python types
# All values in python have a type
# Classes define new types (e.g. and instance of class Stuff is of type Stuff)

# consider a class
class Stuff:
    def __init__(self, name):
        self.name = name
        
    def bar(self):
        print("bar")

# It has three components
"""
1. Name ("Stuff")
2. Base classes (In this case type by default)
3. Functions (__init__, bar)
"""
print(type(int)) # class type
print(type(list)) # class type
print(isinstance(Stuff, type)) # True

# So classes are instances of types
# Then type must be a class somewhere
print(type)


# How the class actually gets created using these three components
body = """
def __init__(self, name):
    self.name = name
    
def bar(self):
    print("bar")
"""
# Make the class dictionary (aka the namespace)
clsdict = type.__prepare__("Stuff", ()) # third arg is a base class if any
print(clsdict) # {}
exec(body, globals(), clsdict)
# populates clsdict
print(clsdict) # {'__init__': <function __init__ at 0x7fe066879630>, 'bar': <function bar at 0x7fe0668797e0>}
Stuff = type("Stuff", (), clsdict)

# This is why everything is a type
s = Stuff("some name")
# Now it becomes class Stuff type
print(type(s))
s.bar()

# So we constructed a class from scratch.
# If we want a class constructed from type (the standard way)
class Stuff(metaclass=type):
    def __init__(self, name):
        self.name = name
        
    def bar(self):
        print("bar")

print(type(Stuff)) # <class 'type'>

# Now, what if you wanted to construct the class in a custom way rather than through type?
# You typically inherit from type and redefine __new__ or __init__

class mytype(type):
    def __new__(cls, name, bases, clsdict):
        if len(bases) > 1:
            raise TypeError("No multiple inheritance")
        clsobj = super().__new__(cls, name, bases, clsdict)
        return clsobj

class Base(metaclass=mytype):
    ...

class Apple(Base): ...
class Pear(Base): ...

try:
    class Orange(Apple, Pear): ...
except TypeError as exc:
    print(exc)
    
# The key point with metaclasses is that you get all the info about the class before it is created with type
# Similar to the class decorator created before
# meta classes -> class hierarchy, impacts the entire chain of classes that inherit


