# Dynamic protocols: Sequence must implement __getitem__ and __len__
# Python manages to iterate and use the in operator using __getitem__ with the absence of __iter__ and __contains__
# When you follow establed protocols you can increase leveraging existing standard library or 3rd party could

# Monkey Patching
# Dynamically changing a module or class at runtime

import collections
class FrenchDeck:
    Card = collections.namedtuple("Card", ["rank", "suit"])
    ranks = [str(n) for n in range(2, 11)] + list("JQKA")
    suits = "spades diamonds clubs hearts".split()

    def __init__(self):
        self._cards = [FrenchDeck.Card(rank, suit) for suit in self.suits for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

from random import shuffle
l = list(range(10))
shuffle(l)
print(l)

try:
    fd = FrenchDeck()
    shuffle(fd)
except TypeError as e:
    # French deck cannot be changed in place (immutable).
    print(e)

# FrenchDeck only implements the immutable sequence protocol.
# It needs to implement __setitem__
# Lets say FrenchDeck is not a class we wrote, then we can monkeypatch __setitem__

def set_card(deck, position, card):
    deck._cards[position] = card

FrenchDeck.__setitem__ = set_card
fd = FrenchDeck()
shuffle(fd)

# Defensive programming => Fail Fast
from collections import abc

def init(iterable):
    list(iterable) # If it is not iterable, then TypeError
    # Or if the data should be copied
    isinstance(iterable, abc.MutableSequence)

# These are examples of duck typing. If class A implements protocol B, then it must be C
# The interface is the special methods the class implements
# Goose typing uses abstract base classes as an interface
# Python does not have the "interface" keyword
# Subclassing ABC's to make it explicit you are implementing a previously defined interface
# Runtime checking using isinstance or issubclass with ABC's rather than concrete classes

from collections import namedtuple, abc

Card = namedtuple('Card', ['rank', 'suit'])

class FrenchDeck2(abc.MutableSequence):
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits
                                        for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

    def __setitem__(self, position, value):  # <1>
        self._cards[position] = value

    def __delitem__(self, position):  # <2>
        del self._cards[position]

    def insert(self, position, value):  # <3>
        self._cards.insert(position, value)


# In FrenchDeck2, we need to implement _delitem__ (abc.MutableSequence) forces us to do this
# Same with insert
# Note that checking against the ABC is not done at import time, but at runtime (when actually instantiating FrenchDeck2)
fd = FrenchDeck2()
fd.pop()

# We implement the abstract methods __getitem__, __setitem__, __delitem__
# In return, because of inheriting abc.MutableSequence we get concrete methods __contains__, __iter__, pop, .. etc. (see page 450) 

# abc's provide flexibility to the caller
# E.g., we are creating an add framework that supports a user provided non-repeating random-picking class
# We can write a custom ABC for our add framework. If the user implements the ABC, we guarantee it will work

import abc

class Tombola(abc.ABC):

    @abc.abstractmethod
    def load(self, iterable):
        """Add items from an iterable"""

    @abc.abstractmethod
    def pick(self):
        """Remove an item at random, returning it
        
        This method should raise 'LookupError' when the instance is empty
        """

    def loaded(self):
        """Return 'True' if there is at least one item, false otherwise"""
        return bool(self.inspect())

    def inspect(self):
        """Return a sorted tuple with the items currently inside"""
        items = []
        while True:
            try:
                items.append(self.pick())
            except LookupError:
                break
        self.load(items)
        return tuple(items)

    # Note that ABC's can still have concrete methods
    # It is ok to have concrete methods IF they only use other methods defined in (not outside) the ABC

# What happens if we do not implement the abc?
class Fake(Tombola):
    def pick(self):
        return 12
    
try:
    f = Fake()
except TypeError as e:
    print(e)

import random

class BingoCage(Tombola):

    def __init__(self, items):
        self._randomizer = random.SystemRandom()    
        self._items = []
        self.load(items)

    def load(self, items):
        self._items.extend(items)
        self._randomizer.shuffle(self._items)

    def pick(self):
        try:
            return self._items.pop()
        except IndexError:
            raise LookupError("pick from empty BingoCage")

    def __call__(self):
        self.pick()

# A virtual subclass of ABC
from random import randrange

@Tombola.register
class TombolaList(list):
    def pick(self):
        if self:
            position = randrange(len(self))
            return self.pop(position)
        else:
            raise LookupError("pop from empty TomboList")
        
    load = list.extend

    def loaded(self):
        return bool(self)

    def inspect(self):
        return tuple(self)

print(issubclass(TombolaList, Tombola))
t = TombolaList(range(100))
print(isinstance(t, Tombola))
print(t.pick())

# The overall point of the virtual subclass seems to be this:
# If we inherit for example abc.Sequence, it doesnt matter if we register it as a virtual subclass or inherited
# Becuase either way we have to implement the interface
# But in the case we have our own abc.ABC e.g. Tombola(abc.ABC), it also implements concrete methods along this the abstract methods
# By creating a virtual subclass, we avoid interiting these concrete methods

# Static Protocols
def double(x):
    print(x * 2)

double(1.5)
double("A")

from fractions import Fraction

double(Fraction(2, 5))

# In duck typing, the type of an object is determined by its behavior
# so in this case, the type is "something" because it implements __mull__

from typing import TypeVar, Protocol

T = TypeVar("T")

class Repeatable(Protocol):
    def __mul__(self: T, repeat_count: int) -> T: ... #In Python, the ellipsis (...) after a function signature is used as a placeholder to indicate that additional code or parameters can be added to the function. 

RT = TypeVar("RT", bound=Repeatable)

def double(x: RT) -> RT:
    return x * 2

# We now have static type checking to make sure the object passed in can be multiplied by an interger
# the type of x is irrelevant as long as it implements __mul__

# The duck typing approach, avoid using isinstance or hasattr. 
# Instead try the operation, and handle the exception as needed.
# Duck typing vs Goose typing (static typing) see page 472

# Runtime checking static protocols

# An ABC with one abstract method __float__
from typing import SupportsFloat

a = 123
print(isinstance(a, SupportsFloat))

# Designing a static protocol
from typing import Protocol, runtime_checkable, Any
# runtime_checkable => can be used with isinstance and issubclass
@runtime_checkable
class RandomPicker(Protocol):
    def pick(self) -> Any: ... # Use this instead of NotImplemented

import random
from typing import Any, Iterable, TYPE_CHECKING

class SimplePicker:
    def __init__(self, items: Iterable) -> None:
        self._items = list(items)
        random.shuffle(self._items)

    def pick(self) -> Any:
        return self._items.pop()

# test is instance
popper: RandomPicker = SimplePicker([1])
assert isinstance(popper, RandomPicker) # Because @runtime_checkable and popper has pick

items = [1, 2]
popper = SimplePicker(items)
item = popper.pick()
assert item in items
# Only viewable in mypy
if TYPE_CHECKING:
    reveal_type(item) # Any


    

    