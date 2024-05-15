# DDD -> Domain Driven Design
# The domain model corresponds to the business logic layer in the three tier model
# The domain is the business problem we are trying to solve through understanding and modeling it

# In this case we are modeling an ecommerce platform that sells furnature.

from datetime import date
from dataclasses import dataclass
from typing import Optional, Set

def test_allocating_to_a_batch_reduces_available_quantity():
    batch = Batch("batch-001", "SMALL-TABLE", qty=20, eta=date.today())
    line = OrderLine("order-ref", "SMALL-TABLE", 2)
    batch.allocate(line)
    assert batch.available_quantity == 18
    
# Using TDD we come up with the test cases based on our mental model of the business
# This test case can be decribed to a non-technical person and they should be able to ...
# agree that it describes the correct behavior in the system.

@dataclass(frozen=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int

class Batch:
    def __init__(self, ref: str, sku: str, qty: int, eta: Optional[date]):
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self.available_quantity = qty

    def allocate(self, line: OrderLine):
        self.available_quantity -= line.qty        


def make_batch_and_line(sku, batch_qty, line_qty):
    return (Batch("batch-001", sku, batch_qty, eta=date.today()), 
            OrderLine("order-123", sku, line_qty))

def test_can_allocate_if_available_greater_than_required():
    large_batch, small_line = make_batch_and_line("ELEGANT-LAMP", 20, 2)
    assert large_batch.allocate(small_line)
    
def test_allocate_if_available_smaller_than_required():
    small_batch, large_line = make_batch_and_line("ELEGANT-LAMP", 2, 20)
    assert small_batch.allocate(large_line) is False

def test_can_allocate_if_available_equal_to_required():
    batch, line = make_batch_and_line("ELEGANT-LAMP", 2, 2)
    assert batch.allocate(line)

def test_cannot_allocate_if_sku_does_not_match():
    batch = Batch("batch-001", "UNCOMFORTABLE-CHAIR", 100, eta=None)
    line = OrderLine("order-123", "EXPENSIVE-TOASTER", 10)
    batch.allocate(line) is False

def test_can_only_deallocate_allocated_line():
    batch, unallocated_line = make_batch_and_line("DECORATIVE-TRINKET", 20, 2)
    batch.deallocate(unallocated_line)
    assert batch.available_quantity == 20


class Batch:
    def __init__(self, ref: str, sku: str, qty: int, eta: Optional[date]):
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self._purchased_quantity = qty
        self._allocations: Set[OrderLine] = set()

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
        return line.sku == self.sku and line.qty <= self.available_quantity
    
def test_allocate_is_idempotent(): # function can be called several times without changing the result.
    batch, line = make_batch_and_line("ANGULAR-DESK", 20, 2)
    batch.allocate(line)
    batch.allocate(line) # silently fails since sku is identical
    assert batch.available_quantity == 18
    
# What is a line though?
# In the business language, and Order has multiple Lines
# An Order has a unique refernce, but a Line does not.
# Whenever we have a business concept that has a value but no identity ...
# we use the Value Object pattern (the business object is uniquely defined by the data it holds)

@dataclass(frozen=True)
class Line:
    orderid: str #OrderReference
    sku: str #ProductReference
    qty: int #Quantity

from typing import NamedTuple
from collections import namedtuple

@dataclass(frozen=True)
class Name:
    first_name: str
    surname: str

class Money(NamedTuple):
    currency: str
    value: int

Line = namedtuple("Line", ["sku", "qty"])

assert Money("gbp", 100) == Money("gbp", 100)
assert Name("Harry", "Percival") != Name("Bob", "Gregory")
assert Line("RED-CHAIR", 5) == Line("RED-CHAIR", 5)

fiver = Money("gbp", 5)
tenner = Money("gbp", 10)

# A value object that should implement behavior like this:
# assert (fiver + fiver) == tenner
# assert (tenner - fiver) == fiver

# import pytest

# with pytest.raises(ValueError):
#     Money("usd", 10) + Money("gbp", 10)
    
# etc ... 

# Note the difference between a value object and a domain object:
# 1. A value object is identified by the uniqueness of its data. It is not a long lived object.
# 2. A domain object is identified by a unique reference id. It is a long lived object and ...
#    is also refered to as an entity.

# For example, a batch is an entity. We can add or remove an OrderLine / Line from Batch ...
# and it is still the same Batch.

class Batch:
    def __init__(self, ref: str, sku: str, qty: int, eta: Optional[date]):
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self._purchased_quantity = qty
        self._allocations: Set[OrderLine] = set()

    def __eq__(self, other: Batch):
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
        return line.sku == self.sku and line.qty <= self.available_quantity
    
# For value objects, the hash should be based on all its value attributes and be immutable
# If you need to use an entity in a dict or set, you can implement hash like above ...
# just make sure this property is read-only.

# What about allocating from multiple Batches?
from datetime import date, timedelta

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)

# Exceptions can express domain concepts too.
class OutOfStock(Exception):
    pass

def allocate(line: OrderLine, batches: list[Batch]) -> str:
    try:
        # Here sorted works by implementing __gt__
        batch = next(b for b in sorted(batches) if b.can_allocate(line))
        batch.allocate(line)
        return batch.reference
    except StopIteration:
        raise OutOfStock(f"Out of stock for sku {line.sku}")

def test_current_stock_batches_to_shipments():
    in_stock_batch = Batch("in-stock-batch", "RETRO-CLOCK", 100, eta=None)
    shipment_batch = Batch("shipment-batch", "RETRO-CLOCK", 100, eta=tomorrow)
    line = OrderLine("oref", "RETRO-CLOCK", 10)
    
    allocate(line, [in_stock_batch, shipment_batch])

    assert in_stock_batch.available_quantity == 90
    assert in_stock_batch.available_quantity == 100

def test_prefers_earlier_batches():
    earliest = Batch("speedy-batch", "MINAMILIST-SPOON", 100, eta=today)
    medium = Batch("nomral-batch", "MINAMILIST-SPOON", 100, eta=tomorrow)
    latest = Batch("slow-batch", "MINAMILIST-SPOON", 100, eta=later)
    line = OrderLine("order1", "MINAMILIST-SPOON", 10)
    
    allocate(line, [earliest, medium, latest])
    
    assert earliest.available_quantity == 90
    assert medium.available_quantity == 100
    assert latest.available_quantity == 100