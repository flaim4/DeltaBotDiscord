import sqlite3
import asyncio
from disnake.ext import commands

class Войс(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect("data.db")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot:
            return
        cur = self.conn.cursor()
        server_id = member.guild.id
        if before.channel is None:
            cur.execute("""SELECT * FROM users WHERE server_id = ? AND user_id = ?""", (server_id , member.id,))
            row = cur.fetchone()
            if row is None:
                cur.execute("""INSERT INTO users (server_id, name, user_id, lvl, xp, balance, time_voice, warning, mes) VALUES (?,?,?,?,?,?,?,?,?)""",
                    (server_id, member.name, member.id, 0, 0, 0, 0, 0, 0))
                self.conn.commit()
                cur.execute("""SELECT * FROM users WHERE server_id = ? AND user_id = ?""", (server_id , member.id,))
                row = cur.fetchone()
            voice_time = row[6]
            while True:
                voice_time +=1
                await asyncio.sleep(1)
                cur.execute("""UPDATE users SET time_voice=? WHERE server_id=? AND user_id=?""", (voice_time, server_id, member.id,))
                self.conn.commit()

                if after.channel is None:
                    return

    def cog_unload(self):
        self.conn.close()
        
def setup(bot):
    bot.add_cog(Войс(bot))
