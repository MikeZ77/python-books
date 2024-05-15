import abc
from allocation.domain import model

class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add(self, product: model.Product):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, sku) -> model.Product:
        raise NotImplementedError


# Once we define certain entities to be aggregagates, then we are conisdered the public entity.
# All entities under/inside it are private. Therefore the aggregate is the only entity that needs a Respository.
# Aggregates are the only way of entering our domain model.
class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session):
        self.session = session

    def add(self, product):
        self.session.add(product)

    def get(self, sku):
        return self.session.query(model.Product).filter_by(sku=sku).first()
