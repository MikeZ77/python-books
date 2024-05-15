from __future__ import annotations
from typing import Optional
from datetime import date

from allocation.domain import model
from allocation.domain.model import OrderLine
from allocation.service_layer import unit_of_work


class InvalidSku(Exception):
    pass


def is_valid_sku(sku, batches):
    return sku in {b.sku for b in batches}


def add_batch(
        ref: str, sku: str, qty: int, eta: Optional[date],
        uow: unit_of_work.AbstractUnitOfWork
):
    with uow:
        uow.batches.add(model.Batch(ref, sku, qty, eta))
        uow.commit()

# UoW acts as a single entrypoint to our persistent storage
# UoW context allows us to complete a transaction, so DB objects are not changing half way through
# I.e. conistant state

def allocate(
        orderid: str, sku: str, qty: int,
        uow: unit_of_work.AbstractUnitOfWork
) -> str:
    line = OrderLine(orderid, sku, qty)
    with uow:
        batches = uow.batches.list()
        if not is_valid_sku(line.sku, batches):
            raise InvalidSku(f'Invalid sku {line.sku}')
        batchref = model.allocate(line, batches)
        uow.commit()
    return batchref
