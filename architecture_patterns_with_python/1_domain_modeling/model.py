from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import Optional, List, Set

# Exceptions can be used to express domain concepts
class OutOfStock(Exception):
    pass


def allocate(line: OrderLine, batches: List[Batch]) -> str:
    try:
        batch = next(
            b for b in sorted(batches) if b.can_allocate(line)
        )
        batch.allocate(line)
        return batch.reference
    except StopIteration:
        raise OutOfStock(f'Out of stock for sku {line.sku}')

# And OrderLine is a ***Value Object** meaning that its id is based on the data it holds
# Note that dataclasses and class(NamedTuple) are useful for Value Objects because they already implement __eq__
@dataclass(frozen=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int

# Batches are ***Entities*** i.e. long lived assets uniquely identifiable through an id (reference).
# Typically we implement __eq__ and can implementent __hash__ if we want to use them in a dict.
# We can change the eta, allocations, and purchased_qty ... but its still the same batch
class Batch:
    def __init__(
        self, ref: str, sku: str, qty: int, eta: Optional[date]
    ):
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self._purchased_quantity = qty
        self._allocations = set()  # type: Set[OrderLine]

    def __repr__(self):
        return f'<Batch {self.reference}>'

    def __eq__(self, other):
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference

    def __hash__(self):
        return hash(self.reference)

    def __gt__(self, other):
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta

    def allocate(self, line: OrderLine):
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate(self, line: OrderLine):
        if line in self._allocations:
            self._allocations.remove(line)

    @property
    def allocated_quantity(self) -> int:
        return sum(line.qty for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity

    def can_allocate(self, line: OrderLine) -> bool:
        return self.sku == line.sku and self.available_quantity >= line.qty


# Encapsulation: We encapsulate (hide behavior) that performs a task using a well defined object or function.
# Abstraction: The object or function itself is an abstraction.
# So, we encapsulate behavior by using some level of abstractions. This can make the code more readable, testable, and easier to maintain.

# Dependency Inversion Principle (DIP) (Part of SOLI*D*)
# 1. High level modules should not depend on low level modules
# 2. Abstractions should not depend on details, instead, details should depend on abstractions.

# Note that when one function, object, or module depends on another, then it *depends* on the other.
# Note that othe language use Interfaces to ABC's to define an abstraction. It can be useful to use ABC's in python, but relying on Duck typing is also fine. 

# Lets look at part 1. of DIP:
# High level modules are the code that your organization cares about and that deal with *real world concepts* ...
# for example, for VOD content, we care about licences and rights for the content. 
# e.g., as a business we would like to create licenses, modify their start and end dates, and assign content to a license.

# Low level modules are for example, maybe we have have to make an API call, or there is some kind of internal validation process.
# Thhe user does not know or care about this, therefore they are low level modules.

# So, the main idea here is that that high level module is an abstraction for the low level module. We should be able to ...
# change the low level module indepently of the high level module without having to change the interface.

# Part 2. of DIP, ... will be exaplained using examples later ...

# The Domain Model
# Contains high level models or busines logic.
# It is a layered approach, we have the business logic layer in front of the persistance layer.
# The domain driven approach means that we care most about the behavior and domain/objet model ...
# The technical details, e.g. storage and DB schema comes after since it is a low level module.

# What is the Domain Model? It is the same as the business logic layer.
# It is there to solve the business problem you have, e.g. How do we license an asset?
