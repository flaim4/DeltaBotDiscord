from disnake.ext import commands
import sqlite3

class message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect("data.db")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        server_id = message.guild.id
        user_id = message.author.id
        name = message.author.display_name
        cur = self.conn.cursor()
        cur.execute('''SELECT * FROM users WHERE server_id = ? AND user_id = ?''',
                    (server_id, user_id,))
        self.conn.commit()
        cur.execute("""SELECT xp, lvl, mes, balance FROM users WHERE server_id=? AND user_id=?""", (message.guild.id, user_id,))
        result = cur.fetchone()
        if result is None:
            cur.execute("""INSERT INTO users (server_id, name, user_id, lvl, xp, balance, time_voice, warning, mes) VALUES (?,?,?,?,?,?,?,?,?)""",
                        (server_id, name, user_id, 0, 0, 0, 0, 0, 0))
            self.conn.commit()
            mes = 0
        else:
            mes = result[2]
            mes += 1
        cur.execute("""UPDATE users SET mes=? WHERE server_id=? AND user_id=?""", (mes, message.guild.id, user_id,))
        self.conn.commit()

    def cog_unload(self):
        self.conn.close()

def setup(bot):
    bot.add_cog(message(bot))