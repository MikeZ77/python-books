import abc
import model


# An abstraction over persistant storage ...
# We treat the persistance layer like memory. We can get and add a domain object while not caring about the implementation
# ... and database specifics like transactions.
class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add(self, batch: model.Batch):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference) -> model.Batch:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session):
        self.session = session

    def add(self, batch):
        self.session.add(batch)

    def get(self, reference):
        # If we want to use raw sql queries, we can use session.execute and model.Batch.__table__ ??? ...
        # to get the table name?
        return self.session.query(model.Batch).filter_by(reference=reference).one()

    def list(self):
        return self.session.query(model.Batch).all()
