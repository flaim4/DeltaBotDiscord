from dataclasses import dataclass
from typing import Dict

@dataclass
class CogsInfo:
    enable : bool

@dataclass
class ConfigService:
    cogs : Dict[str, CogsInfo]
    command_prefix : str
    