# The Repository object sits between the Domain model and the Database.
# The idea of dependency inversion is that a higher level module should depend on an abstraction of the ...
# lower level module, and not the implementation.

# In the case of crating our persistance layer we do not want our domain model (the complex logic) to depend ...
# on the lower level database layer
# So for example we dont want to define OrderLine as something like this:

from sqlalchemy import Column, ForeignKey, Integer, String, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, mapper

Base = declarative_base()

class Order(Base):
    id = Column(Integer, primary_key=True)

class OrderLine(Base):
    id = Column(Integer, primary_key=True)
    sku = Column(String(250))
    ...
    order_id = Column(Integer, ForeignKey("order.id"))
    order = relationship(Order)


# Instead we want the ORM to depend on the domain model and seperate them
from _1_domain_modeling import OrderLine, Batch

metadata = MetaData()

order_lines = Table("order_lines", metadata,
                Column("id", Integer, primary_key=True, autoincrement=True),
                Column("sku", String(255)),
                Column("qrt", Integer, nullable=False),
                Column("orderid", String(255))
                )

def start_mappers():
    lines_mapper = mapper(OrderLine, order_lines)


# Once mapped, we can easily load and save the domain model.
# As mentioned the repository layer sits between the domain and the persistance layer.
# It acts as an abstraction over the persistance layer s.t. we can call methods like we are working in memoery.

# The simplest repository layer we can create implements just the add and get methods:
from abc import ABC, abstractmethod

class AbstractRepository(ABC):
    @abstractmethod
    def add(self, batch: Batch):
        raise NotImplementedError

    @abstractmethod
    def get(self, reference) -> Batch:
        raise NotImplementedError

# Authors notes: ABC's can be ignored, and they need to be maintained ...
# ABC's are an example of goose typing (e.g. making the protocol explicit ...
# and checking types during runtime) ...

# The authors often just rely on python duck typing ... in this case any object ...
# with add() and get() is an AbstractRepository

# Using Protocols is another option what could be preferable beause it uses ...
# composition rather than inheritance.

# So whats the cost of creating this layer of abstraction ... every time we need a new ...
# domain object / entity, we need to implement its repository.
# The benefit is that we get a simple abstraction over our storage layer ... this decoupling ...
# makes it easy to change the way we store things without impacting the domain layer (ependency inversion)





