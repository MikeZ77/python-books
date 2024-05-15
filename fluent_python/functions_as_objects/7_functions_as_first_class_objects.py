# 1. Created at runtime
# 2. Can be assigned to a variable or element in a data structue
# 3. Can be passed as an arument to a function
# 4. Can be returned as a result from another function

def factorial(n):
    """ returns n! """
    return 1 if n <= 1 else n * factorial(n-1)

print(factorial(5))
print(factorial.__doc__)
print(type(factorial))

fact = factorial
print(list(map(fact, range(10))))

# Higher Order Functions = take a function as an argument OR returns a function as the result
# Some of the best known higher order functions are map, filter, reduce, and apply
# However, these traditional functional programming functions have some better python alternatives

# replacing map with a list comp
print(list(map(fact, range(5))))
print([fact(i) for i in range(5)])

# Now what if we only want the even 
print(list(map(fact, filter(lambda n: n % 2, range(5)))))
print([fact(i) for i in range(5) if i % 2])

from functools import reduce
from operator import add

print(reduce(add, range(100)))
print(sum(range(100)))

# Other reducing built-ins
print(all([True, False, False])) # Returns True if all Truthy
print(any([True, False, False]))# Returns True if any Truthy

# Anonomous functions
# Throw away functions
# Good for trivial tasks, but avoid complicated lambdas

cats = ["grey", "brown", "orange"]
print(sorted(cats, key=lambda cat: cat[::-1]))

# The nine flavors of callable objects
# The callable operator () may be used on more than just functions
# User defined callable types

import random

class BingoCage:
    def __init__(self, items):
        self._items = list(items)
        random.shuffle(self._items)

    def pick(self):
        try:
            return self._items.pop()
        except IndexError:
            raise LookupError("Picked from an empty BingoCage")

    def __call__(self):
        return self.pick()

bingo = BingoCage(range(3))
print(bingo.pick())
# Shortcut by creating a function-like object
print(bingo())

# From positional to keyword-only parameters
# 1 positonal, all other positionals, a keyword only arg b/c it comes after all positionals,
# finally all other keyword args
def tag(name, *content, class_=None, **attrs): 
    """Generate one or more HTML tags"""
    if class_ is not None:
        attrs['class'] = class_
    attr_pairs = (f' {attr}="{value}"' for attr, value
                    in sorted(attrs.items()))
    attr_str = ''.join(attr_pairs)
    if content:
        elements = (f'<{name}{attr_str}>{c}</{name}>'
                    for c in content)
        return '\n'.join(elements)
    else:
        return f'<{name}{attr_str} />'
    
# To specify only keyworkd args
def only_keywords(*, a, b, c=None):
    print(a, b, c)

only_keywords(a=1, b=2)

# Using partial to bind pre-determined function args
from operator import mul
from functools import partial
triple = partial(mul, 3) # Now 3 will alays be the first arg to mul
print(triple(7)) # => 21
