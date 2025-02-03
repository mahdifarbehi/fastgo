import traceback
from pydantic import BaseModel
from sqlalchemy import text

from backbone.base_class import Base
from backbone.base_exceptions import (
    DuplicateException,
    IntegrityException,
    NotFoundException,
)
from unit_of_work import UnitOfWork
from sqlalchemy.exc import IntegrityError


class BaseService:

    @staticmethod
    def create(cls: type[Base], data: BaseModel) -> dict:
        with UnitOfWork() as uow:
            obj: Base = cls.create(**data.model_dump())
            uow.session.add(obj)
            try:
                uow.commit()
                return obj.to_dict()
            except IntegrityError:
                traceback.print_exc()
                uow.rollback()
                raise DuplicateException(detail="Object already exists")

    @staticmethod
    def read_one(cls, id) -> dict:
        with UnitOfWork() as uow:
            obj: Base = uow.main_repo.read_one(cls, id)
            if not obj:
                raise NotFoundException(id)
            return obj.to_dict()

    @staticmethod
    def read_all(cls) -> list[dict]:
        with UnitOfWork() as uow:
            objs: list[Base] = uow.main_repo.read_all(cls)
            return [obj.to_dict_basic() for obj in objs]

    @staticmethod
    def update(cls, id, data: BaseModel) -> dict:
        with UnitOfWork() as uow:
            obj: Base = uow.main_repo.read_one(cls, id)
            if not obj:
                raise NotFoundException(id)
            obj.update(**data.model_dump())
            uow.session.add(obj)
            try:
                uow.commit()
                return obj.to_dict()
            except IntegrityError:
                traceback.print_exc()
                uow.rollback()
                raise DuplicateException(detail="Object already exists")

    @staticmethod
    def delete(cls, id) -> dict:
        with UnitOfWork() as uow:
            obj: Base = uow.main_repo.read_one(cls, id)
            if not obj:
                raise NotFoundException(id)
            uow.session.delete(obj)
            try:
                uow.commit()
                return id
            except IntegrityError:
                uow.rollback()
                raise IntegrityException()

    @staticmethod
    def read_one_query(id, query) -> dict | None:
        with UnitOfWork() as uow:
            query_result = uow.session.execute(text(query), {"id": id}).fetchone()
            if not query_result:
                raise NotFoundException(id)
            return query_result._asdict()

    @staticmethod
    def read_all_query(query) -> list[dict]:
        with UnitOfWork() as uow:
            query_result = uow.session.execute(text(query)).fetchall()
            if not query_result:
                return []
            return [row._asdict() for row in query_result]
