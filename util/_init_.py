from disnake.ext.commands import Cog, Bot
from abc import ABC, abstractmethod
import logging
from util.event import bus
from dataclasses import dataclass

def Indelifer(id: str):
    def decorator(obj):
        obj.id = id
        return obj
    return decorator

class CogBase(Cog):
    def __init__(self, bot : Bot, name : str):
        self.bot : Bot = bot
        bot.add_cog(self)
        self.logger : logging.Logger = logging.getLogger(name)
        
    @abstractmethod
    async def init(self) -> None:
        pass
    
@dataclass
class CogPostInit:
    cog : CogBase