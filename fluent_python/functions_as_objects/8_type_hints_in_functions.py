# Gradual typing system
# Mypy => checks annotated python code
# Gradual because it is optional and does not catch type errors at runtime
# Sometimes type hints can be too complicated to complicated code. It is ok to simplify or ship without.

def show_count(count: int, word: str) -> str:
    if count == 1:
        return f"1 {word}"
    count_str = str(count) if count else "no"
    return f"{count_str} {word}s"

# poetry run mypy data_structures/8_type_hints_in_functions.py
# If a func signature has no annotions mypy ignores it by default

from pytest import mark

@mark.parametrize("qty, expected", [(1, "1 part"), (2, "2 parts")])
def test_show_count(qty, expected):
    got = show_count(qty, "part")
    assert got == expected

def test_show_count_zero():
    got = show_count(0, "part")
    assert got == "no parts"

# poetry run mypy --disallow-incomplete-defs data_structures/8_type_hints_in_functions.py
from typing import Iterable, Optional

# plural may be a string or none type
def show_count_plural(count: int, singular: str, plural: Optional[str] = None) -> str:
    if count == 1:
        return f'1 {singular}'
    count_str = str(count) if count else 'no'
    if not plural:
        plural = singular + 's'
    return f'{count_str} {plural}'

# Types are defined by supported operations
# what are the valid types of x?
def double(x):
    return x * 2
# numeric, sequence, str, or a type hat inherits or implements __mul__

from collections import abc

# Unsupported operand types for * ("Sequence[Any]" and "int")
def double_double(x: abc.Sequence):
    return x * 2

# Does not work because abc.Sequence does not implement or inherit __mul__
# The Any Type
def double(x):
    return x * 2

from typing import Any

def double(x: Any) -> Any:
    return x * 2

def double(x: object) -> object:
    return x * 2

# This function also accepts an arg of any type, becuase every type is a sub-type of object
# But object does not support __mul__
# Object has fewer operations than abc.Sequence which supports fewer operations than list.
# A class T2 that inherits from T1, then T2 is a sub-type of T1  

# Optional[str] == Union[str, None] or str | None
# If possible, avoid returning Union, becuase it forces the user to check the type

# Abstract Base Classes (ABC)
from collections.abc import Mapping
# abc.Mapping allows the called to use dict, defaultdict, ChainMap, etc.
# def name2hex(name: str, color_map: Mapping[str,int]) -> str:

# The idea is be liberal in what we accept, but conservative in what we return
# The return type should be a concrete type
# Another example, under typing.List => useul for annotating return types
# To annotate arguments, it is preffered to use an abstract collection type like Sequence or Iterable

from typing import TypeAlias
FromTo: TypeAlias = tuple[str, str]

from collections.abc import Sequence
from random import shuffle
from typing import TypeVar
T = TypeVar("T")

def sample(population: Sequence[T], size: int) -> list[T]:
    if size < 1:
        raise ValueError("size must be >= 1")
    result = list(population)
    shuffle(result)
    return result[:size]

# Difference between T and Any => T must be all the same type
# What if we need to restrict T? 
from decimal import Decimal
from fractions import Fraction
NumberT = TypeVar("NumberT", float, Decimal, Fraction)

def mode(data: Iterable[NumberT]) -> NumberT:
    pass

# What is the difference between NumberT and Iterable[float | Decimal | Fraction]?
# With T, it must be the same type in that scope, so if T is float it must return float
# With Union, Iterable[float] -> Decimal is allowed

# Bounded TypeVar
from collections.abc import Iterable, Hashable
def mode(data: Iterable[Hashable]) -> Hashable:
    pass

# We return hash Hashable, so the type checker will only let us call hash() on what is returned 
# We can specify any sub-type of Hashable instead
HashableT = TypeVar("HashableT", bound=Hashable)
def mode(data: Iterable[HashableT]) -> HashableT:
    pass

# Like
class SomeType(Hashable):
    pass

# Static protocols
# The type checker verifies the protocol is implemented
# However, the class does not need to inherit, register, or declare the abc that defines the protocol
T = TypeVar("T")

def top(series: Iterable[T], length: int) -> list[T]:
    ordered = sorted(series, reverse=True)
    return ordered[:length]

# Here T can be any objcet
# But what if it does not implement "<" operator?
# If we are sorting, we need that

from typing import Protocol, Any
class SupportsLessThan(Protocol):
    def __lt__(self, other: Any) -> bool:
        return self < other
    

from typing import Callable
# Callable[[Param1, Param2, ...], Return]
