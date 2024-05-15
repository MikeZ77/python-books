from collections import OrderedDict
from typing import Any


class LastUpdatedOrderedDict(OrderedDict):
    def __setitem__(self, __key: Any, __value: Any) -> None:
        super().__setitem__(__key, __value)
        self.move_to_end(__key)

# Problems with overriding built-in types
class DoubleDict(dict):
    def __setitem__(self, key: Any, value: Any) -> None:
        return super().__setitem__(key, [value] * 2)

dd = DoubleDict(one=1) # When there is not init, I guess the init of dict user its own __setitem__?
print(dd)
dd["two"] = 2
print(dd) # {'one': 1, 'two': [2, 2]}
dd.update(three=3)
print(dd) # {'one': 1, 'two': [2, 2], 'three': 3}

class AnswerDict(dict):
    # Always return 42
    def __getitem__(self, key):
        return 42

ad = AnswerDict(a="foo")
print(ad["a"]) #42
d = {}
d.update(ad) 
# When you pass a dict to update instead of kwargs, it uses __getitem__
# But it uses the __getitem__ of d, so we loose the value
print(d) #{'a': 'foo'}

# Now if we subclass collections.UserDict, these issues do not happen
from collections import UserDict # primarily used for subclassing

class DoubleDict(UserDict):
    def __setitem__(self, key: Any, value: Any) -> None:
        return super().__setitem__(key, [value] * 2)

dd = DoubleDict(one=1)
print(dd)
dd["two"] = 2
print(dd)
dd.update(three=3)
print(dd)
#{'one': [1, 1]}
#{'one': [1, 1], 'two': [2, 2]}
#{'one': [1, 1], 'two': [2, 2], 'three': [3, 3]}

# Summary: You probably want the behavior seen in inheriting UserDict rather than dict

# Multiple Inheritance and Method Resolution Order
# The diamond problem, naming conflicts when superclass implement a method of the same name
# Which method does the subclass get?

class Root:
    def ping(self):
        print(f"{self}: ping() in root")
    
    def pong(self):
        print(f"{self}: pong() in root")

    def pie(self):
        print("pie is called root")

    def __repr__(self):
        cls_name = type(self).__name__
        return f"<instance of {cls_name}"

class A(Root): 
    def ping(self):
        print(f'{self}.ping() in A')
        super().ping()

    def pong(self):
        print(f'{self}.pong() in A')
        super().pong()

    def pie(self):
        print("Pie is called A")


class B(Root):
    def ping(self):
        print(f'{self}.ping() in B')
        super().ping()

    def pong(self):
        print(f'{self}.pong() in B')

class Leaf(A, B):
    def ping(self):
        print(f'{self}.ping() in Leaf')
        super().ping()

leaf = Leaf()
leaf.ping()
print()
leaf.pong()

# The order of multiple inheritance works like this:
# ping: Leaf super().ping() -> A super().ping() -> B super().ping() -> Root ping()
# pong: A super().ping() (called through inheritance) -> B ping() (does not call super)

class U: # U inherits directly from object, not Root
    def ping(self):
        print(f'{self}.ping() in U')
        super().ping()

class Leaf(U, A):
    def ping(self):
        print(f'{self}.ping() in Leaf')
        super().ping()

print()
u = U()
try:
    u.ping()
except AttributeError as e:
    print(e) # 'super' object has no attribute 'ping' -> since object does not have ping

leaf = Leaf()
leaf.ping()

"""
<instance of Leaf.ping() in Leaf
<instance of Leaf.ping() in U
<instance of Leaf.ping() in A
<instance of Leaf: ping() in root
"""
# But now U cooperates with A, since super() refers to A here
leaf.pie()

# Mixin Classes
import collections

def _upper(key):
    try:
        return key.upper()
    except AttributeError:
        return key
    
class UpperCaseMixin:
    def __setitem__(self, key, item):
        super().__setitem__(_upper(key), item)

    def __getitem__(self, key):
        return super().__getitem__(_upper(key))
    
    def get(self, key, default=None):
        return super().get(_upper(key), default)

    def __contains__(self, key):
        return super().__contains__(_upper(key))
    
# so UpperCaseMixin depends on a sibling that that implements or inherits methods with the same signature

class UpperDict(UpperCaseMixin, collections.UserDict): ...

class UpperCounter(UpperCaseMixin, collections.Counter): ...

# So mixins are designed to be subclassed together with at least one other class (sibling)
# They are designed to customize the behavior of the sibling class
    
d = UpperDict([("a", "Capital A"), (2, "2 does not have upper()")])
print(d)

c = UpperCounter("DAfddefeS")
print(c) # UpperCounter({'D': 3, 'F': 2, 'E': 2, 'A': 1, 'S': 1})
print(c.most_common()) # [('D', 3), ('F', 2), ('E', 2), ('A', 1), ('S', 1)]

# In general, using multiple inheritance is not the norm, it can be confusing
# Coping with inheritance
# 1. Favor object composition over inheritance
"""
Subclassing is a form of tight coupling. Issues can arise when adding a class to the inheritance higharchy (.e.g name clashes).
Instead, hold reference to whatevr object/class and delegate its methods.
"""
# 2. Understand why inheritance is used
"""
Inheritance creates an is-a relationship best done with ABC's
Inheritance avoids code duplication and re-use.
"""
# 3. If a class is intended to define an interface, use using abc.ABC or typing.Protocol
# 4. Use explicit Mixins for code re-use. i.e. a Mixin that can be used for multiple classes
"""
A Mixin should never be instantiated
A concrete class should never inherit from a Mixin
Each Mixin should implement a single specific behavior
There is no formal way for Python to state that a class is Mixin, so naming that class with a Mixin suffix makes it more clear
""" 
# 5. Avoid subclassing concrete classes



