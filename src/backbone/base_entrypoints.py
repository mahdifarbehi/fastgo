from typing import Type
from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel

from backbone.base_class import Base
from backbone.base_utils import Entity
from backbone.base_service import BaseService
from backbone.base_utils import OBJECT_DICT
from backbone.base_utils import OBJECT_DICT_HINTS
from pydantic_core._pydantic_core import ValidationError


router = APIRouter(prefix="/api/generic", tags=["generic"])


def pydantic_data_maker(cls: type[BaseModel], data: dict):
    try:
        return cls(**data)
    except ValidationError:
        raise HTTPException(status_code=400, detail="wrong json data")


@router.post("/{class_name}")
def generic_create_api(
    class_name: Entity,
    data: dict = Body(..., examples=[OBJECT_DICT_HINTS]),
):
    generic_class: Type[Base] = OBJECT_DICT[class_name]
    pydantic_class = generic_class.request_class_builder()
    pydantic_data = pydantic_data_maker(pydantic_class, data)
    result = BaseService.create(generic_class, pydantic_data)
    return result


@router.get("/{class_name}/{id}")
def generic_read_one_api(
    class_name: Entity,
    id: int,
):
    result = BaseService.read_one(OBJECT_DICT[class_name], id)
    return result


@router.get("/{class_name}")
def generic_read_all_api(class_name: Entity):
    result = BaseService.read_all(OBJECT_DICT[class_name])
    return result


@router.put("/{class_name}/{id}")
def generic_update_api(
    class_name: Entity,
    id: int,
    data: dict = Body(..., examples=[OBJECT_DICT_HINTS]),
):
    generic_class: Type[Base] = OBJECT_DICT[class_name]
    pydantic_class = generic_class.request_class_builder(crud="update")
    pydantic_data = pydantic_data_maker(pydantic_class, data)
    result = BaseService.update(generic_class, id, pydantic_data)
    return result


@router.delete("/{class_name}/{id}")
def generic_delete_api(
    class_name: Entity,
    id: int,
):
    result = BaseService.delete(OBJECT_DICT[class_name], id)
    return result
