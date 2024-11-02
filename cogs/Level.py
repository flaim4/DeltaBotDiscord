
import disnake 
from disnake import Embed
from disnake.ext import commands 

from disnake.interactions.application_command import ApplicationCommandInteraction

import random

from util.db import Data
import util.Reaction 

def action_level_up_defult(role : int = None):
    async def up(msg : disnake.Message, level : int):
        await msg.channel.send(f"<@{msg.author.id}>, Level Up {level}!")
        if role != None:
            msg.author.add_roles(msg.guild.get_role(role))
    return up

actionmap = {}

def property(level : int):
    def wappeler(func):
        actionmap[level] = func
        return func
    return wappeler

async def level_up(level: int, message: disnake.Message):
    if level in actionmap:
        action = actionmap[level]
        if action:
            await action(message, level)

    
property(5)(action_level_up_defult(1301971636203028501))
property(10)(action_level_up_defult(1301978683828863000))
property(15)(action_level_up_defult(1301978745049059338))
property(20)(action_level_up_defult(1301978767811547267))
property(30)(action_level_up_defult(1301978796978602044))
property(50)(action_level_up_defult(1301978830801473576))


class Level(commands.Cog):
    def __init__(self, bot : commands.Bot) -> None:
    
        self.cur = Data.getCur()
        self.bot = bot
        self.bot.add_cog(self)

    @commands.Cog.listener(disnake.Event.message)
    async def on_message(self, message : disnake.Message):
        if (message.author.id == self.bot.user.id): return
        await util.Reaction.addReaction(message=message)
        await self.add_xp(server_id=message.guild.id, user_id=message.author.id, xp=self.calculate_xp(message=message.content), msg=message)
        
    def calculate_xp(self, message):
        return (min(len(message) // 10, 50) + random.randint(5, 15))

    async def add_xp(self, server_id : int, user_id : int, xp : int, msg : disnake.Message):
        self.cur.execute("SELECT lvl, xp FROM Users WHERE server_id = ? AND user_id = ?", (server_id, user_id))
        result = self.cur.fetchone()

        if result:
            current_level, current_xp = result
            new_xp = current_xp + xp
            xp_for_next_level = 100 * current_level

            while new_xp >= xp_for_next_level:
                new_xp -= xp_for_next_level
                current_level += 1
                await level_up(current_level, msg)
                xp_for_next_level = 100 * current_level

            self.cur.execute("""
                UPDATE Users 
                SET message = message + 1, xp = ?, lvl = ? 
                WHERE server_id = ? AND user_id = ?
            """, (new_xp, current_level, server_id, user_id))
        else:
            self.cur.execute("""
                INSERT INTO Users (server_id, user_id, message, xp, lvl)
                VALUES (?, ?, 1, ?, 0)
            """, (server_id, user_id, xp))

        Data.commit()