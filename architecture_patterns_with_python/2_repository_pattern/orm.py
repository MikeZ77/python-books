from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date,
    ForeignKey
)
from sqlalchemy.orm import mapper, relationship

import model

# The ORM exists to bridge the conceptual gap between domain modeling and objects and databases and relations.
# Recall Dependency Inversion, our domain model should not depend on a lower level module.
# An ORM is useful becuase we do not care how the model is persisted.

# If you use SQLAlchemy in the traditional way you get something like this:
############################################################################
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class LineItem(Base):
    id = Column(Integer, primary_key=False)
 
############################################################################

# Our domain model is heavily dependent on the ORM (it inherits from Base an ORM class)...
# But our model is not supposed to know or care about the database
# We need to invert the dependency

# The solution is to define the schema seperately, and apply a mapper (map it to) our domain model.
# This is also called imperitive mapping.

metadata = MetaData()
# We define our database table schema
order_lines = Table(
    'order_lines', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('sku', String(255)),
    Column('qty', Integer, nullable=False),
    Column('orderid', String(255)),
)

batches = Table(
    'batches', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('reference', String(255)),
    Column('sku', String(255)),
    Column('_purchased_quantity', Integer, nullable=False),
    Column('eta', Date, nullable=True),
)

allocations = Table(
    'allocations', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('orderline_id', ForeignKey('order_lines.id')),
    Column('batch_id', ForeignKey('batches.id')),
)

# We have SQLAlchemy map order_lines Table to our model.OrderLine
def start_mappers():
    lines_mapper = mapper(model.OrderLine, order_lines)
    mapper(model.Batch, batches, properties={
        '_allocations': relationship(
            lines_mapper,
            secondary=allocations,
            collection_class=set,
        )
    })
