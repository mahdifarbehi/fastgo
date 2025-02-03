from datetime import datetime
from typing import Type

import sqlalchemy as sa
import sqlalchemy.orm as sao
from pydantic import BaseModel, Field

from backbone.base_exceptions import ValueErrorException


class Base(sao.DeclarativeBase):
    id: sao.Mapped[int] = sao.mapped_column(primary_key=True)
    created_at: sao.Mapped[datetime] = sao.mapped_column(default=sa.func.now())
    ignored_fields: list = ["id", "created_at"]
    field_defaults: dict = {}

    @classmethod
    def create(cls, **kwargs):
        try:
            return cls(**kwargs)
        except TypeError as e:
            raise ValueErrorException(detail=str(e))

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if value is not None:
                setattr(self, key, value)

    def to_dict(self):
        return {
            c.key: getattr(self, c.key)
            for c in sa.inspection.inspect(self).mapper.column_attrs
        }

    def to_dict_basic(self):
        return self.to_dict()

    @classmethod
    def request_class_builder(cls, crud: str = "create") -> Type[BaseModel]:

        dynamic_fields: dict = {}
        update_dynamic_fields: dict = {}
        annotations: dict = {}

        for field_name, field in vars(cls).items():
            if field_name in cls.ignored_fields:
                continue
            if isinstance(field, sao.attributes.InstrumentedAttribute):
                column_type = field.type.python_type
                annotations[field_name] = column_type

                update_dynamic_fields[field_name] = Field(default=None)

                if field_name in cls.field_defaults.keys():
                    dynamic_fields[field_name] = Field(
                        default=cls.field_defaults[field_name]
                    )
                else:
                    if field.nullable:
                        dynamic_fields[field_name] = Field(default=None)
                    else:
                        dynamic_fields[field_name] = Field(...)

        result_fields = (
            update_dynamic_fields.copy() if crud == "update" else dynamic_fields.copy()
        )
        return type(
            cls.__name__ + "RequestModel",
            (BaseModel,),
            {
                "__annotations__": annotations,
                **result_fields,
            },
        )
