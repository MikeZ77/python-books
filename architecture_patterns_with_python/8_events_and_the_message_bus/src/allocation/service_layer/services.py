from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from datetime import date

from allocation.domain import model
from allocation.domain.model import OrderLine
if TYPE_CHECKING:
    from . import unit_of_work


class InvalidSku(Exception):
    pass


def add_batch(
        ref: str, sku: str, qty: int, eta: Optional[date],
        uow: unit_of_work.AbstractUnitOfWork
):
    with uow:
        product = uow.products.get(sku=sku)
        if product is None:
            product = model.Product(sku, batches=[])
            uow.products.add(product)
        product.batches.append(model.Batch(ref, sku, qty, eta))
        uow.commit()

# Michael: We want to send an email when we are out of stock. 
# Recall the service layer is like an orchistration layer, so it may seem like it should go here ...
# product.allocate -> can raise OutOfStock ... we send the email and re-raise the error.
# The problem is that this break the single responsibility principle, out domain layer allocate() should not be 
# responsible for sending emails.
# Also, sending an email directly is an implementation detail and we would like the service layer to depend on abstractions.

def allocate(
        orderid: str, sku: str, qty: int,
        uow: unit_of_work.AbstractUnitOfWork
) -> str:
    line = OrderLine(orderid, sku, qty)
    with uow:
        product = uow.products.get(sku=line.sku)
        if product is None:
            raise InvalidSku(f'Invalid sku {line.sku}')
        batchref = product.allocate(line)
        uow.commit()
        return batchref
