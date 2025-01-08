import json as js
from types import SimpleNamespace

def loadJsonObject(name : str):
    with open(f"data/{name}.json", encoding='utf-8') as fs:
        return js.load(fs, object_hook=lambda d: SimpleNamespace(**d))

def loadJson(name : str):
    with open(f"data/{name}.json", encoding='utf-8') as fs:
        return js.load(fs)
