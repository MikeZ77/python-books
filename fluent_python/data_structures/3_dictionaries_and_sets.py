# Dict comprehensions
DIAL_CODES = [
        (86, 'China'),
        (91, 'India'),
        (1, 'United States'),
        (62, 'Indonesia'),
        (55, 'Brazil'),
        (92, 'Pakistan'),
        (880, 'Bangladesh'),
        (234, 'Nigeria'),
        (7, 'Russia'),
        (81, 'Japan'),
    ]

d = {country: code for code, country in DIAL_CODES}
print(d)

def dump(**kwargs):
    print(kwargs)

dump(**{"a": 1}, b=2, **{"c": 3})
print({"a": 1, "b": 2, **{"b": 3, "c": 4}}) # The last duplicate key to get unpacked overrides
d1 = {"a": 1, "b": 2}
d2 = {"a": 2, "b": 4, "c": 6}
print(d1 | d2) # d1 gets overriden by d2
d1 |= d2
print(d1) # Merge mapping in-place

# An object is hashable if it has a hash code that never changes during its lifetime
# Must implement __hash__ and __eq__ (can be compared)
# Immutable types and primitives are hashable, mutable types are not

# Handling a missing key
l = {}
l.setdefault("a", []).append(1)
print(l)

# How to handle missing keys
from collections import defaultdict
d = defaultdict(list)
print(d["a"])

# The __missing__ method
# Not built into dict, but you can subclass it. When dict calls __getitem__ it will call __missing__ instead of generating a KeyError
class MyDict(dict):
    def __missing__(self, key):
        self[key] = []

d = MyDict()
d["a"]
print(d["a"])

from collections import ChainMap
d1 = {"a": 1, "b": 3}
d2 = {"a": 2, "b": 4, "c": 6}
chain = ChainMap(d1, d2)
print(chain["c"])
print(chain)
print(chain["a"])
chain["c"] = -1
print(chain) # Changes only effect the first input mapping
print(chain["c"])

from collections import Counter
a = Counter("asdvsvsvdbth")
print(a)
print(a["s"])
a.update("sacdgvsdvrgver")
print(a)
print(a.most_common(3))

from collections import UserDict

class StrKeyDict(UserDict):
    def __missing__(self, key):
        if isinstance(key, str):
            raise KeyError(key)
        return self[str(key)]

    def __contains__(self, key):
        return str(key) in self.data

    def __setitem__(self, key, item):
        self.data[str(key)] = item

#Sets
# Simple use case, remove duplicates:
l = ["spam", "ham", "spam", "spam"]
l = list(set(l))
print(l)
# Preserve order
l = list(dict.fromkeys(l).keys())
print(l)

a = {1, 2, 3, 4}
a.remove(1)
print(a)

a = frozenset([1, 2, 3, 4])
print(a)

a = {chr(a) for a in range(100)}
print(a)

d1 = {}
d2 = {"a": 1, "b": 2}
d1.update(d2)
print(d1)