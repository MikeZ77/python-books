from __future__ import annotations

import model
from model import OrderLine
from repository import AbstractRepository

class InvalidSku(Exception):
    pass

# This is the service layer
# Its job is to handle an outside request and to ORCHISTRATE and operation.
# E.g.
# 1. Get some data from the database
# 2. Update the domain model
# 3. Persist any changes

def is_valid_sku(sku, batches):
    return sku in {b.sku for b in batches}

def allocate(line: OrderLine, repo: AbstractRepository, session) -> str:
    batches = repo.list()
    if not is_valid_sku(line.sku, batches):
        raise InvalidSku(f'Invalid sku {line.sku}')
    batchref = model.allocate(line, batches)
    session.commit()
    return batchref

# Note that there can also be a "Domain Layer"
# The domain layer would be responsible for some piece of logic that belongs to the domain model ... 
# but doesn't sit naturally inside a value object or entity (i.e. it is not stateful)