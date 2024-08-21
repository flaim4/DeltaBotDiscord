import disnake 
from disnake.ext import commands
from disnake import TextInputStyle
import sqlite3
import time
from util.balance import Balance
import settings
from disnake import colour

from util.db import Data

class isMessage(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.cur = Data.getCur()
        
    @commands.Cog.listener()
    async def on_message(self, message):
        self.cur.execute("""SELECT * FROM Users WHERE server_id = ? AND user_id = ?""", (message.guild.id, message.author.id))
        row = self.cur.fetchone()
        if row:
            result = row[2]
            res = result + 1
            self.cur.execute("""UPDATE Users SET message = ? WHERE server_id = ? AND user_id = ?""", (res, message.guild.id, message.author.id))
            Data.commit()
        else: 
            self.cur.execute("""INSERT INTO Users (server_id, user_id, message) VALUES (?, ?, ?)""",
                            (message.guild.id, message.author.id, 1))
            Data.commit()
            return 1

def setup(bot):
    bot.add_cog(isMessage(bot))