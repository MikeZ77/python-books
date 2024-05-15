# The python interpreter invokes special methods to perform fundamental language constructs.
# If we want our objects to support and interact with fundamental language constructs, we need to implement these special methods.
# These special methods are also known as dunder methods

import collections
 
# We use collections.namedtuple to build class of object that are just attributes and have no custom methods (like a database record)
Card = collections.namedtuple("Card", ["rank", "suit"])
class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list("JQKA")
    suits = "spades diamonds clubs hearts".split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

deck = FrenchDeck()
print(len(deck))
print(f"Second element: {deck[1]}")

from random import choice
# Because our class implements __getitem__ and __len__, it is an iterable and can be used with the standard library
print(f"Random choice: {choice(deck)}")

# Because it is an iterable we can iterate:
for card in deck:
    print(card)

# Because it is an iterable we can check if an object exists:
print(Card(rank='7', suit='spades') in deck)

import math

class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Vector(x={self.x}, y={self.y})"

    def __abs__(self):
        return math.hypot(self.x, self.y)

    def __bool__(self):
        # Note: bool checks __bool__ if available, else __len__
        return bool(abs(self))

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)


a = Vector(1, 2)
b = Vector(0, 0)
c = a + b
print(c)
# Note that bool is rarely needed since any object can be used in a boolean context
print(bool(b))

    