import copy
import enum
import disnake
from disnake.ext import commands
import random
from util.db import Data
import util.Reaction
import util.Resouces as res
from types import SimpleNamespace
from typing import Dict, List, Callable, Awaitable, Tuple
from dataclasses import dataclass
import asyncio
import re

url_pattern = r'https?://(?:www\.)?[\w.-]+(?:\.[a-z]{2,})+[/\w.-]*'

lock = asyncio.Lock()

def format_strings_in_object(obj, args):
    if isinstance(obj, str):
        return obj.format(*args)
    elif isinstance(obj, list):
        return [format_strings_in_object(item, args) for item in obj]
    elif isinstance(obj, dict):
        return {key: format_strings_in_object(value, args) for key, value in obj.items()}
    elif hasattr(obj, "__dict__"):
        for attr, value in obj.__dict__.items():
            setattr(obj, attr, format_strings_in_object(value, args))
        return obj
    return obj

async def LDsend(level: int, message: disnake.Message, data : SimpleNamespace) -> int:
    print("Dsend")
    return 0

async def Lsend(level: int, message: disnake.Message, data : SimpleNamespace) -> int:
    data = copy.copy(data)
    format_strings_in_object(data, (level, message))
    await message.channel.send(embed=disnake.Embed.from_dict(data.__dict__))
    return 0

async def LDMsend(level: int, message: disnake.Message, data : SimpleNamespace) -> int:
    data = copy.copy(data)
    format_strings_in_object(data, (level, message))
    await message.author.send(embed=disnake.Embed.from_dict(data.__dict__))
    return 0

async def Lrole(level: int, message: disnake.Message, data : SimpleNamespace) -> int:
    if hasattr(data, "id"):
        await message.author.add_roles(message.guild.get_role(data.id))
        return 0
    return 1

async def LRrole(level: int, message: disnake.Message, data : SimpleNamespace) -> int:
    try:
        if hasattr(data, "id"):
            await message.author.remove_roles(message.guild.get_role(data.id))
            return 0
        return 1
    except:
        return 0

class ActionType(enum.Enum):
    SEND = 0
    ADD_ROLE = 1
    SEND_DEFULT = 2
    SEND_DM = 3
    REMOVE_ROLE = 4

    @staticmethod
    def get(name : str) -> enum.Enum:
        if name in ["#", "SEND", "send", "message", "MESSAGE", "msg", "MSG"]:
            return ActionType.SEND
        elif name in ["#D", "#d", "SENDD", "sendd", "messaged", "MESSAGED", "msgd", "MSGD"]:
            return ActionType.SEND_DM
        elif name in ["$", "add_role", "ADDROLE", "addrole", "ADD_ROLE", "role", "ROLE"]:
            return ActionType.ADD_ROLE
        elif name in ["$R", "remove_role", "REMOVEDROLE", "removerole", "REMOVE_ROLE", "rrole", "RROLE"]:
            return ActionType.REMOVE_ROLE
        elif name in ["^"]:
            return ActionType.SEND_DEFULT
        raise ValueError(f"Invalid ActionType name: {name}")

    @staticmethod
    def get_function(type : enum.Enum) -> Callable[[int, disnake.Message, SimpleNamespace], Awaitable[int]]:
        if type == ActionType.SEND:
            return Lsend
        elif type == ActionType.ADD_ROLE:
            return Lrole
        elif type == ActionType.SEND_DEFULT:
            return LDsend
        elif type == ActionType.SEND_DM:
            return LDMsend
        elif type == ActionType.REMOVE_ROLE:
            return LRrole

@dataclass
class Action:
    type : enum.Enum
    data : SimpleNamespace

def compile() -> Tuple[List[Action], Dict[int, List[Action]]]:
    meta = res.loadJsonObject("level")
    data : Tuple[List[Action],Dict[int, List[Action]]] = ([Action(ActionType.get("#"), SimpleNamespace())], {})
    for obj in meta:
        ldata = []
        for ob2 in obj.actions:
            ldata.append(Action(ActionType.get(ob2.type), ob2.data))
        data[1][obj.level] = ldata
    return data

data = compile()

async def level_up(level: int, message: disnake.Message):
    actions : List[Action] = data[1].get(level, data[0])
    if not (actions is None):
        for action in actions:
            result : int = (await (ActionType.get_function(action.type))(level, message, action.data))
            if result == 0:
                continue
            elif result == 1:
                print(f"Level : {level}, Action : {action.type} {action.data} | Missing argumets")
            elif result == 2:
                print(f"Level : {level}, Action : {action.type} {action.data} | Missing Fatal")




class Level(commands.Cog):
    def __init__(self, bot : commands.Bot) -> None:
        self.cur = Data.getCur()
        self.bot = bot
        self.bot.add_cog(self)

    @commands.Cog.listener(disnake.Event.message)
    async def on_message(self, message : disnake.Message):
        if (message.author.id == self.bot.user.id): return
        await util.Reaction.addReaction(message=message)
        async with lock:
            await self.add_xp(server_id=message.guild.id, user_id=message.author.id, xp=self.calculate_xp(message=message.content), msg=message)
        
    def calculate_xp(self, message):
        message = re.sub(url_pattern, '', message)
        return (min((len(message) + 1) // 10, 50) + random.randint(5, 15))

    async def add_xp(self, server_id : int, user_id : int, xp : int, msg : disnake.Message):
        self.cur.execute("SELECT lvl, xp FROM Users WHERE server_id = ? AND user_id = ?", (server_id, user_id))
        result = self.cur.fetchone()

        if result:
            current_level, current_xp = result
            new_xp = current_xp + xp
            xp_for_next_level = 150 * current_level

            while new_xp >= xp_for_next_level:
                new_xp -= xp_for_next_level
                current_level += 1
                await level_up(current_level, msg)
                xp_for_next_level = 150 * current_level

            if current_level == None:
                return
            self.cur.execute("""
                UPDATE Users 
                SET message = message + 1, xp = ?, lvl = ? 
                WHERE server_id = ? AND user_id = ?
            """, (new_xp, current_level, server_id, user_id))
        else:
            self.cur.execute("""
                INSERT OR REPLACE INTO Users (server_id, user_id, message, xp, lvl)
                VALUES (?, ?, 1, ?, 0)
            """, (server_id, user_id, xp))

        Data.commit()