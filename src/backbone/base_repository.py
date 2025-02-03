from sqlalchemy.orm.session import Session


class MainRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, object):
        self.session.add(object)

    def read_one(self, cls, id):
        return self.session.query(cls).filter_by(id=id).one_or_none()

    def read_all(self, cls):
        return self.session.query(cls).all()
