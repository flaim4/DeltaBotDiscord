import random
import disnake 
import json

from typing import Dict
from utility.main import *
from disnake.ext import commands
from utility.logs_tools import *
from main import log

class Log(commands.Cog):

    def __init__(self, bot: commands.Bot):
       self.bot: commands.Bot = bot
       self.welcome: json.load = load_json()

    @commands.Cog.listener()
    async def on_message_edit(self, before: disnake.Message, after: disnake.Message) -> None: 
        print_log(f"The message has been edited Member: {before.author.display_name}({before.author.id}) Before: {before.content} After: {after.content}")
        log.write_log(f"The message has been edited Member: {before.author.display_name}({before.author.id}) Before: {before.content} After: {after.content}")

    @commands.Cog.listener()
    async def on_message_delete(self, message: disnake.Message) -> None: 
        print_log(f"The message has been deleted Member: {message.author.display_name}({message.author.id}) Deleted message: {message.content}")
        log.write_log(f"The message has been deleted Member: {message.author.display_name}({message.author.id}) Deleted message: {message.content}")

    @commands.Cog.listener()
    async def on_member_join(self, member: disnake.Member) -> None: 
        print_log(f"{member.name}, join in {member.guild.name}")
        log.write_log(f"{member.name}, join in {member.guild.name}")
    
    @commands.Cog.listener()
    async def on_member_leave(self, member: disnake.Member) -> None: 
        print_log(f"{member.name}, join in {member.guild.name}")
        log.write_log(f"{member.name}, join in {member.guild.name}")

