import disnake 
from disnake.ext import commands
import sqlite3
import json
import os

class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    


def setup(bot):
    bot.add_cog(Shop(bot))    