# A container sequence holds references to the objects it contains
# A flat sequence stores the value (restricted to holding primitive types)

# Listcomps are more readable than map and filter
symbols = '$¢£¥€¤'
beyond_ascii = [ord(s) for s in symbols if ord(s) > 127]
print(beyond_ascii)
beyond_ascii = list(filter(lambda c: c > 127, map(ord, symbols)))
print(beyond_ascii)

# Listcomps for cartesian products
colors = ['black', 'white']
sizes = ['S', 'M', 'L']
tshirts = [(color, size) for color in colors #outer
                         for size in sizes]  #inner

# Listcomps are good for building lists, everything else can use a genexp
symbols = '$¢£¥€¤'
beyond_ascii = tuple(ord(s) for s in symbols) # If the genexp is the only arg, no need to duplicate parenthesis 

import array
# Any array is like a list but the types are constrained
beyond_ascii = array.array("I", (ord(s) for s in symbols)) # Ctype code 
print(beyond_ascii)

# Tuples are immutable lists but can also be used as records (with no field names)
# Record => the meaning of each field is given by its position
# Only the references in a tuple are immutable, not the object itself
a = (10, "alpha", [1,2])
b = (10, "alpha", [1,2])
print(a == b)
b[-1].append(99)
print(a == b)

# An unhashable tuple cannot be used as a dict key or in a set
b = (10, "alpha", (1,2))
try:
    # print(hash(a))
    print(hash(b))
except TypeError:
    print("Not hashable")

# Tuples support all list methods that do not involve adding or removing items
# Unpacking:
# Variable assignment
lax_coordinates = (33.9425, -118.408056)
latitude, longitude = lax_coordinates
# Swapping variables without using a temp variable
latitude, longitude = longitude, latitude
#Unpacking function arguments
t = (20, 8)
print(divmod(*t))
# Unpacking function return values
import os
_, filename = os.path.split("/home/michael/my_file.txt")
print(filename)
# Using * to grab excess items
# We can do this wil parallel assignment
a, b, *rest = range(5)
print(rest)
print(type(rest)) # list
a, b, *rest = range(2)
print(rest) # []
# It can also appear in any position
a, *body, b, c = range(6)
print(body) #[1, 2, 3]
*head, b, c = range(6)
print(head) #[0, 1, 2, 3]
# In function calls we can unpack multiple times
def fun(a, b, c, d, *rest):
    print(a, b, c, d, rest)

fun(*[1, 2], 3, 4, *range(5, 7))
# Nested unpacking

metro_areas = [
    ('Tokyo', 'JP', 36.933, (35.689722, 139.691667)),
    ('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889)),
    ('Mexico City', 'MX', 20.142, (19.433333, -99.133333)),
    ('New York-Newark', 'US', 20.104, (40.808611, -74.020386)),
    ('São Paulo', 'BR', 19.649, (-23.547778, -46.635833)),
]

def main():
    print(f'{"":15} | {"latitude":>9} | {"longitude":>9}')
    for name, _, _, (lat, lon) in metro_areas:
        if lon <= 0:
            print(f'{name:15} | {lat:9.4f} | {lon:9.4f}')
main()

# Unpacking into a list, when you know you only have a single value
# This is also known as destructuring
[val] = ["cat"]
print(val)
print(type(val)) # str
[[val]] = [["cat"]]
print(val)
print(type(val)) # str
# You can also unpack using a tuple
val, ["cat"]
print(val)
print(type(val)) # str
((val,),) = [["cat"]]
print(val)
print(type(val)) # str
# Note that single item tuples must be written with a trailing comma

# Pattern Matching: Even more powerful way to unpack sequences
# match/case python3.10
def main():
    print(f'{"":15} | {"latitude":>9} | {"longitude":>9}')
    for record in metro_areas:
        match record: # The subject
            case [name, _, _, (lat, lon)] if lon <= 0: # Destructuring the sequence pattern, and the second part is an optional guard
                print(f'{name:15} | {lat:9.4f} | {lon:9.4f}')
main()
# A sequence pattern matches if:
# 1. the subject is a sequence
# 2. The subject and the pattern have the same number of elements
# 3. Each corresponding item matches including nested items

# So for the pattern [name, _, _, (lat, lon)], it matches a sequence with 4 items where the last item is a tuple
# We can make pattern matching more specific by adding type information
# _ means match any single value
record = ["Shanghai", "CN", 24.9, (31.1, 121.3)]
match record:
    case [str(name), _, _, tuple(coords)]:
        print("MATCH!")

# EG, match any sequence that starts with a string, and ends with a tuple:
match record:
    case [str(name), *_, tuple(coords)]:
        print("MATCH!")

# With a guard:
match record:
    case [str(name), *_, tuple(coords)] if coords[0] > 30:
        print("MATCH!")

# SLICING
# All sequence types support sclicing
# Assigning to slices
l = list(range(10))
l[2:5] = "a"
print(l)
del l[3:15]
print(l)
# The right hand side must be an iterable object
# Sequences support + and *
# This always creates a new object
l = [1, 2, 3]
print(hex(id(l)))
print(hex(id(l * 3)))
a = [[]] * 3
print(a)
print([hex(id(l)) for l in a]) # Watch out ... it copied the same array for each element

# how to build a list of lists
board = [["_"] * 3 for _ in range(3)]
print(board)
board[1][1] = "X"
print(board)

# implements __iadd__ and __imul__
l = [1, 2, 3]
print(id(l))
l *= 2 
print(id(l)) # same object
t = (1, 2, 3)
print(id(t))
t *= 2
print(id(t)) # new object

# Sorting
# Functions or methods that change an object in-place should return None
a = [1, 2, 3, 4, 5, 6]
a.sort()
print(a)
print(sorted(a, reverse=True))
print(sorted(a, key=str))

# If a list only contains numbers, then array.array is more optimal
from collections import deque
dq = deque(range(10), maxlen=10)
print(dq)
dq.rotate(3)
print(dq)
dq = deque(range(10), maxlen=10)
dq.rotate(-3)
print(dq)
dq.appendleft(1)
dq.append(1)
print(dq)

