import json as js
import yaml as ya
from types import SimpleNamespace as sn
from dataclasses import is_dataclass, fields
from typing import Dict, get_origin, get_args

def loadJsonObject(name : str):
    with open(f"data/{name}.json", encoding='utf-8') as fs:
        return js.load(fs, object_hook=lambda d: sn(**d))

def loadJson(name : str):
    with open(f"data/{name}.json", encoding='utf-8') as fs:
        return js.load(fs)
    
def from_dict(cls, data):
    if not is_dataclass(cls) or not isinstance(data, dict):
        return data

    kwargs = {}
    for field in fields(cls):
        value = data.get(field.name)
        field_type = field.type

        origin = get_origin(field_type)
        args = get_args(field_type)

        if is_dataclass(field_type):
            value = from_dict(field_type, value)
        elif origin is dict:
            key_type, val_type = args
            value = {
                key: from_dict(val_type, val) for key, val in value.items()
            }
        else:
            value = from_dict(field_type, value)

        kwargs[field.name] = value

    return cls(**kwargs)

def dict_to_namespace(d):
    if isinstance(d, dict):
        return sn(**{k: dict_to_namespace(v) for k, v in d.items()})
    elif isinstance(d, list):
        return [dict_to_namespace(i) for i in d]
    else:
        return d

def loadYamlObject(name: str):
    with open(f"data/{name}.yaml", encoding='utf-8') as fs:
        data = ya.load(fs, Loader=ya.FullLoader)
        return dict_to_namespace(data)

def loadYaml(name: str):
    with open(f"data/{name}.yaml", encoding='utf-8') as fs:
        return ya.load(fs, Loader=ya.FullLoader)