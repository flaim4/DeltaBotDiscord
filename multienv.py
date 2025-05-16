import json
import os
from typing import Dict, List, Optional
import configparser
import logging

logger = logging.getLogger(__name__)

class EnvProvider:
    def load(self) -> None:
        pass
    def reload(self) -> None:
        pass
    def get(self, key : str, category : Optional[str] = "base") -> Optional[str]:
        pass

    def setGlobal(self):
        os.getEnv = self.get
        os.env_provider = self

    def __format__(self, format_spec):
        parts = format_spec.split(":")
        if len(parts) != 2:
            raise ValueError("The format should be of the type 'category:key'")
        category, key = parts
        result = self.get(key, category)
        return result if result is not None else "Not found"

class IniEnvProvider(EnvProvider):
    interpolation: configparser.Interpolation = configparser.ExtendedInterpolation()
    def __init__(self, file : str, encoding: Optional[str] = "utf-8"):
        super().__init__()
        self.file = os.path.abspath(file)
        self.config = configparser.ConfigParser(interpolation=IniEnvProvider.interpolation)
        self.encoding = encoding

    def load(self) -> None:
        if os.path.exists(self.file):
            self.config.read(self.file, encoding=self.encoding)
        else:
            self.config.add_section("base")
            with open(self.file, 'w', encoding=self.encoding) as configfile:
                self.config.write(configfile)

    def reload(self) -> None:
        self.config = configparser.ConfigParser(interpolation=IniEnvProvider.interpolation)
        self.load()

    def get(self, key : str, category : Optional[str] = "base") -> Optional[str]:
        try:
            return self.config.get(category, key)
        except:
            return None

class CategoryDictEnvProvider(EnvProvider):
    def __init__(self, data : Dict[str, Dict[str, str]]):
        super().__init__()
        self.data : Dict[str, Dict[str, str]] = data

    def get(self, key: str, category: Optional[str] = "base") -> Optional[str]:
        try:
            return self.data[category][key]
        except:
            return None

class DictEnvProvider(EnvProvider):
    def __init__(self, data : Dict[str, str]):
        super().__init__()
        self.data : Dict[str, str] = data

    def get(self, key: str, category: Optional[str] = "base") -> Optional[str]:
        try:
            return self.data[category+key]
        except:
            return None

class PropertiesEnvProvider(DictEnvProvider):
    def __init__(self, file: str, encoding: Optional[str] = "utf-8"):
        super().__init__({})
        self.file = os.path.abspath(file)
        self.encoding = encoding

    def load(self) -> None:
        if os.path.exists(self.file):
            with open(self.file, 'r', encoding=self.encoding) as file:
                for line in file:
                    line = line.strip()
                    if not line or line.startswith('#') or line.startswith('!'):
                        continue
                    key, value = line.split('=', 1)
                    self.data[key.strip()] = value.strip()
        else:
            with open(self.file, 'w', encoding=self.encoding) as configfile:
                configfile.write(f"#Auto Create\n#file:{self.file}\n#encoding:{self.encoding}")

    def reload(self) -> None:
        self.data = {}
        self.load()


class JsonEnvProvider(CategoryDictEnvProvider):
    def __init__(self, file: str, encoding: Optional[str] = "utf-8"):
        super().__init__({})
        self.file = os.path.abspath(file)
        self.encoding = encoding

    def load(self) -> None:
        if os.path.exists(self.file):
            self.data = json.load(open(self.file, encoding=self.encoding))
        else:
            self.data["base"] = {}
            with open(self.file, 'w', encoding=self.encoding) as configfile:
                json.dump(self.data, configfile)

    def reload(self) -> None:
        self.data = {}
        self.load()

providers_pool = {
    "ini": IniEnvProvider,
    "json": JsonEnvProvider,
    "properties": PropertiesEnvProvider
}

class EnvMannager(EnvProvider):
    def __init__(self, providers : Optional[List[EnvProvider]] = []):
        self.providers : List[EnvProvider] = providers

    def load(self) -> None:
        for p in self.providers:
            p.load()

    def reload(self) -> None:
        for p in self.providers:
            p.reload()

    def get(self, key: str, category: Optional[str] = "base") -> Optional[str]:
        for p in self.providers:
            t = p.get(key, category)
            if t is not None:
                return t
        return None

    def AddProvider(self, provider : Optional[EnvProvider] = None, file : Optional[str] = None, type : Optional[str] = None) -> Optional[EnvProvider]:
        if provider is not None:
            self.providers.append(provider)
            return provider
        if file is not None and type is not None:
            provider = providers_pool.get(type, IniEnvProvider)(file)
            self.providers.append(provider)
            return provider
        return None

    def __add__(self, other):
        if isinstance(other, EnvProvider):
            self.providers.append(other)
        elif isinstance(other, tuple) and all(isinstance(item, str) for item in other):
            self.providers.append(providers_pool.get(other[1], IniEnvProvider)(other[0]))
        return self

    def __len__(self):
        return len(self.providers)