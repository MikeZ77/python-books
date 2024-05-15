# The basic idea is:
# 1. define a group or family of algorithms 
# 2. encapsulate some kind of algorithm or business logic s.t. their use is interchangable
# 3. Lets the algorithm vary independently from the client

# Note that the algorithm can be selected at runtime or chosen for the client at runtime ...
# based on some state or current conditions. 

from __future__ import annotations
from collections.abc import MutableSequence
from random import randint

class ValidateItems:
    def __get__(self, cls, _):
        return cls.items_

    def __set__(self, cls, items): # ValidateItems, Sort, items
        first, *rest = items
        if not all(isinstance(item, type(first)) for item in rest):
            raise TypeError("All objects provided must be the same type.")
        cls.items_ = items
        
class Sort:
    # Lets use a descriptior to validate:
    # https://docs.python.org/3/howto/descriptor.html
    items = ValidateItems()
    
    def __init__(self, items: MutableSequence):
        self.items = items

    def __call__(self):
        if len(self.items) < 100:
            return self.insertion_sort()
        else:
            return self.quick_sort(self.items)
    
    def validate_type(self, type_, items):
        if not all(isinstance(item, type_) for item in items):
            raise TypeError("All objects provided must be the same type.")

    def insertion_sort(self):
        for i in range(1, len(self.items)):
            key = self.items[i]
            j = i - 1
            while j >= 0 and key < self.items[j]:
                self.items[j + 1] = self.items[j]
                j -= 1
            self.items[j + 1] = key   
        return self.items
    
    def quick_sort(self, items):
        if len(items) <= 1:
            return items
        else:
            pivot = items[0]
            less = [x for x in items[1:] if x <= pivot]
            greater = [x for x in items[1:] if x > pivot]
            return self.quick_sort(less) + [pivot] + self.quick_sort(greater)  



if __name__ == "__main__":
    l = Sort([randint(-100, 100) for _ in range(1, 50)])
    a = l()
    print(a)
    l = Sort([randint(-100, 100) for _ in range(1, 1000)])
    a = l()
    print(a)