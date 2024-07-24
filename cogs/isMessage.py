import disnake 
from disnake.ext import commands
from disnake import TextInputStyle
import sqlite3
import time
from util.balance import Balance
import settings
from disnake import colour

class isMessage(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.con = sqlite3.connect("member.db")
        self.cur = self.con.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS Users (server_id INTEGER, user_id INTEGER, message INTEGER DEFAULT 0, voice_activ INTEGER DEFAULT 0, warns INTEGER DEFAULT 0, lvl INTEGER DEFAULT 1, xp INTEGER DEFAULT 0)""")

    @commands.Cog.listener()
    async def on_message(self, message):
        self.cur.execute("""SELECT * FROM Users WHERE server_id = ? AND user_id = ?""", (message.guild.id, message.author.id))
        row = self.cur.fetchone()
        if row:
            result = row[2]
            res = result + 1
            self.cur.execute("""UPDATE Users SET message = ? WHERE server_id = ? AND user_id = ?""", (res, message.guild.id, message.author.id))
            self.con.commit()
        else: 
            self.cur.execute("""INSERT INTO Users (server_id, user_id, message) VALUES (?, ?, ?)""",
                            (message.guild.id, message.author.id, 1))
            self.con.commit()
            return 1

def setup(bot):
    bot.add_cog(isMessage(bot))