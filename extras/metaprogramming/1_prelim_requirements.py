"""
Contains some basic python info before getting into metaprogramming
"""

# Defaults are set once at definiton time.

# it is almost always bad to use mutable objects as defaults, since default values are set at definition time
def func(a=[]):
    a.append(4)
    print(a)

func(a=[1, 2, 3])
func() # [4]

# instead use None
def func(a=None):
    if not a:
        a = []
    print(a)

func(a=[1, 2, 3])
func()

# when calling a func with args and kwargs, everything called with "=" is added to kwargs
def func(*args, **kwargs):
    print(args, kwargs)

func(1, 2, 3, x=1, y=2, z=3)

# Also we can use * in the function signature to force kwargs (seen this many times) 

# The concept of a closure (a function that makes and returns a function) 
def make_adder(x, y):
    def add():
        return x + y
    return add

# Like a code generator
adder = make_adder(1, 2)
print(adder())

# classes: instance variable, class variable, instance method, etc.

class Spam:
    def instance_method(self):
        print(self)

    @classmethod
    def class_method(cls):  
        print(cls)

    @staticmethod
    def static_method():
        ...


s = Spam()
s.instance_method()
Spam.class_method()
Spam.static_method()

# Special methods
#__getitem__, __getattr__ etc.

# The python object system is layered heavily on dictionaries
class Spam:
    def __init__(self):
        self.a = 1
        self.b = 2

s = Spam()
print(s.__dict__) # {'a': 1, 'b': 2}
