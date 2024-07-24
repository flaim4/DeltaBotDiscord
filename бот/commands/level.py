from disnake.ext import commands
import sqlite3


class Level_up(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.con = sqlite3.connect("data.db")
        self.cur = self.con.cursor()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        author = message.author.id
        server_id = message.guild.id

        self.cur.execute("""SELECT * FROM users WHERE user_id = ? AND server_id = ?""", (author, server_id))
        row = self.cur.fetchone()

        if row is None:
            self.cur.execute("""INSERT INTO users (user_id , server_id) VALUES (? , ?)""", (author, server_id))
            self.con.commit()
            self.cur.execute("""SELECT * FROM users WHERE user_id = ? AND server_id = ?""", (author, server_id))
            row = self.cur.fetchone()
            xp = row[4]
            lvl = row[3]
            
        xp = row[4]

        lvl = row[3]

        message1 = message.content
        
        num = 0
        
        if message1.startswith('http://') or message1.startswith('https://'):
            xp +=int(1)
            self.cur.execute("""UPDATE users SET xp = ? WHERE user_id = ? AND server_id = ?""", (xp , author, server_id))
            self.con.commit()
            return
        
        
        for n in message1:
            if n == " ":
                continue
            num +=1
        num /=5
   
        xp +=int(num)
        self.cur.execute("""UPDATE users SET xp = ? WHERE user_id = ? AND server_id = ?""", (xp , author, server_id))
        self.con.commit()
        # Количество xp до нового уровня
        level_up_threshold = int(10 * (2 ** lvl))
        if xp >= level_up_threshold:
            lvl +=1
            xp = 0
            self.cur.execute("""UPDATE users SET lvl = ? , xp = ? WHERE user_id = ? AND server_id = ?""", (lvl , xp, author, server_id))
            self.con.commit()
        


def setup(bot):
    bot.add_cog(Level_up(bot))