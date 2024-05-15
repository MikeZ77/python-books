# Overloaded signatures
import functools
import operator
from collections.abc import Iterable
from typing import overload, Union, TypeVar

T = TypeVar("T")
S = TypeVar("S")

@overload
def sum(it: Iterable[T]) -> Union[T, int]: ...              # May return int if the iterable is empty

@overload
def sum(it: Iterable[T], /, start: S) -> Union[T, S]: ...  

# E.g. the max function: Returns the largest item in an iterable or the largest of two or more arguments

MISSING = object()
EMPTY_MSG = "max() arg is an empty sequence"

def max(first, *args, key=None, default=MISSING):
    if args:
        # get max from args
        series = args
        candidate = first
    else:
        # get max from iterable
        series = iter(first)
        try:
            candidate = next(series)
        except StopIteration:
            # The first arg iterable has no elements => return default if provided
            if default is not MISSING:
                return default
            raise ValueError(EMPTY_MSG)
    if key is None:
        # get max
        for current in series:
            if candidate < current:
                candidate = current
    else:
        # The iterable can be objects of type T
        # Pass a callable key to get the value needed to compare
        candidate_key = key(candidate)
        for current in series:
            current_key = key(current)
            if candidate_key < current_key:
                candidate = current
                candidate_key = current_key
    return candidate
 
# How can we type annotate this?
from collections.abc import Callable, Iterable
from typing import Protocol, Any, TypeVar, overload, Union

class SupportsLessThan(Protocol):
    def __lt__(self, other: Any) -> bool: ...

T = TypeVar("T")
LT = TypeVar("LT", bound=SupportsLessThan)
DT = TypeVar("DT")

MISSING = object()
EMPTY_MSG = "max() arg is an empty sequence"

# 1
@overload
def max(__arg1: LT, __arg2: T, *args: LT, key: None = ...) -> LT: ...

# 2
@overload
def max(__arg1: T, __arg2: T, *args: T, key: Callable[[T], LT]) -> T: ...

# 3
@overload
def max(__iterable: Iterable[LT], *, key: None = ...) -> LT: ...

# 4
@overload
def max(__iterable: Iterable[T], *, key: Callable[[T], LT]) -> T: ...

# 5
@overload
def max(__iterable: Iterable[LT], *, key: None = ..., default: DT) -> Union[LT, DT]: ...

# 6 
@overload
def max(__iterable: Iterable[T], *, key: Callable[[T], LT], default: DT) -> Union[T, DT]: ...

def max(first, *args, key=None, default=MISSING):
    if args:
        # get max from args
        series = args
        candidate = first
    else:
        # get max from iterable
        series = iter(first)
        try:
            candidate = next(series)
        except StopIteration:
            # The first arg iterable has no elements => return default if provided
            if default is not MISSING:
                return default
            raise ValueError(EMPTY_MSG)
    if key is None:
        # get max
        for current in series:
            if candidate < current:
                candidate = current
    else:
        # The iterable can be objects of type T
        # Pass a callable key to get the value needed to compare
        candidate_key = key(candidate)
        for current in series:
            current_key = key(current)
            if candidate_key < current_key:
                candidate = current
                candidate_key = current_key
    return candidate

# The key benefit of @overload is clearly defining the return type for the possible inputs that can be passed.

# (#1 #3) Args OR Iterbale that implement SupportsLessThan but key and default not provided
# Note that if args is passed, there must be at least 2, thats what __arg2: T denotes
print(max(1, 2))  
print(max(1, 2, -3))  
print(max([1, 2, -3]))  

# (#2 #4) Argument key provided but no default
print(max(1, 2, -3, key=abs)) #-3
print(max(["Python", "Rust", "Ruby"], key=len)) # Python

# #5 Argument default provided, bu no key
# Returns type in iterable or type of default
print(max([1, 2, -3], default=None))  #LT
print(max([], default=None)) #DT

# #6 Argument key and default provided
print(max([1, 2, -3], key=abs, default=None)) #LT
print(max([], key=abs, default=None)) #DT

# Takeaways: type hints allow Mypy to flag a call like max([None, None]) because None does not implement the SupportsLessThan Protocol

# TypedDict => Type hinsts for dictionaries with a fixed set of keys
books = {
        'isbn': '0134757599',
        'title': 'Refactoring, 2e',
        'authors': ['Martin Fowler', 'Kent Beck'],
        'pagecount': 478,
    }

from typing import TypedDict

class BookDict(TypedDict):
    isbn: str
    title: str
    authors: list[str]
    pagecount: int

# Note that TypedDict is not a dataclass builder. It has no impact at runtime and is only useful for static type checkers and type hints
pp = BookDict(**books)
print(pp) # {'isbn': '0134757599', 'title': 'Refactoring, 2e', 'authors': ['Martin Fowler', 'Kent Beck'], 'pagecount': 478}
print(type(pp)) # <class 'dict'>

# Without mypy, really only useful for documentation. With mypy it adds type checking.
# Other than that not overly useful.

# Type Casting
# Is one way we can handle type checking malunctions or incorrect type hints
# Pointless example just to illustrate:
from typing import cast
a = 10
b = cast(str, a)
print(type(b)) # Still an int

# Sometimes a library has an incorrect type. 
# Too many cast is a code smell since we are basically telling the type checker what a type is.

# Types are added as annotations
def foo(a: int, b:str) -> list[str]:
    return [b * a]

print(foo.__annotations__) # {'a': <class 'int'>, 'b': <class 'str'>, 'return': list[str]}

# This is needed if we refer to a type before it is actually defined.
class Rectangle:
    def stretch(self, factor: float) -> "Rectangle":
        ...


# Implementing a Generic Class
# Recall the Tombola ABC for classes tha work like a Bingo Cage
# LottoBlower is a concrete implementation

import abc

class Tombola(abc.ABC):  # <1>

    @abc.abstractmethod
    def load(self, iterable):  # <2>
        """Add items from an iterable."""

    @abc.abstractmethod
    def pick(self):  # <3>
        """Remove item at random, returning it.

        This method should raise `LookupError` when the instance is empty.
        """

    def loaded(self):  # <4>
        """Return `True` if there's at least 1 item, `False` otherwise."""
        return bool(self.inspect())  # <5>

    def inspect(self):
        """Return a sorted tuple with the items currently inside."""
        items = []
        while True:  # <6>
            try:
                items.append(self.pick())
            except LookupError:
                break
        self.load(items)  # <7>
        return tuple(items)
    
    
import random

from collections.abc import Iterable
from typing import TypeVar, Generic

T = TypeVar("T")

class LottoBlower(Tombola, Generic[T]):
    def __init__(self, items: Iterable[T]) -> None:
        self._balls = list[T](items)
        
    def load(self, items: Iterable[T]) -> None:
        self._balls.extend(items)

    def pick(self) -> T:
        try:
            position = random.randrange(len(self._balls))
        except ValueError:
            raise LookupError("picked from empty LottoBlower")
        return self._balls.pop(position)

    def loaded(self) -> bool:
        return bool(self._balls)

    def inspect(self) -> tuple[T, ...]: # The ... indicates that the tuple can store an aribitrary number of T
        return tuple(self._balls)
    
blower = LottoBlower[int](range(10))
a = blower.pick()
print(a)
print(blower.inspect())

# Recall variance in callback types:
from collections.abc import Callable

def update(probe: Callable[[], float], display: Callable[[float], None]) -> None:
    temperature = probe()
    display(temperature)

def probe_ok() -> int:
    return 42

def display_wrong(temperature: int) -> None:
    print(hex(temperature))

update(probe_ok, display_wrong)

# Notice how probe expects a Callable that returns float, but prob_ok returns an int
# our probe_ok is still consistant with Callable[[], float] becuase returning an int does not break code expecting a float 
# This is because an int can ALWAYS be used in place of a float (i.e. whree a float is expected)

# formally, Callable[[], int] is a subtype of Callable[[], float] since int is a subtype of float
# This means that Callable is covariant on the return type because of this suptype relation between int and float

#TODO Get back to this on page 548

