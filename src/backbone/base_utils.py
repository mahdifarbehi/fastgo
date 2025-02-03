from enum import Enum
from backbone.base_class import Base


def dict_purifier(dct: dict):
    pure_dict = {}
    for k, v in dct["properties"].items():
        key = k
        value = v.get("format", v.get("type", None))
        if not value:
            enum_title = v.get("$ref").split("/")[-1]
            value = dct["$defs"][enum_title]["enum"]
        pure_dict[key] = value
    return pure_dict


class Entity(str, Enum):
    BASE = "base"


OBJECT_DICT = {"base": Base}


OBJECT_DICT_HINTS = {
    k: dict_purifier(v.request_class_builder().model_json_schema())
    for k, v in OBJECT_DICT.items()
}
