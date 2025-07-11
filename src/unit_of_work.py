from sqlalchemy.orm.session import Session

from backbone.base_repository import MainRepository
from project_orm import DEFAULT_SESSION_FACTORY


class UnitOfWork:
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self) -> "UnitOfWork":
        self.session: Session = self.session_factory()
        self.main_repo = MainRepository(session=self.session)
        return self

    def __exit__(self, *args):
        self.rollback()
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()


def get_unit_of_work():
    return UnitOfWork()
