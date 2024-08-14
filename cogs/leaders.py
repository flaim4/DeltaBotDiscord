import disnake
import sqlite3
from util.member import Member
from disnake.ext import commands
import settings

class Leaders(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect('member.db')
        self.cursor = self.conn.cursor()
        self.ProfileColor = settings.InvisibleColor
        
    @commands.slash_command()
    async def leaders(self, ctx):
        self.cursor.execute("SELECT * FROM Users")
        rows = self.cursor.fetchall()

        rows.sort(key=lambda row: row[3], reverse=True)

        text = "### Лидеры по времени в голосовом канале\n"
        limit = 15 

        for index, row in enumerate(rows[:limit], start=1):
            voice_time = row[3]

            if voice_time is None or voice_time == 0:
                days, hours, minutes, seconds = 0, 0, 0, 0
            else:
                days, hours, minutes, seconds = Member.convert_seconds(voice_time)

            if index == 1:
                medal = "🥇"
            elif index == 2:
                medal = "🥈"
            elif index == 3:
                medal = "🥉"
            else:
                medal = f"**{index}.**"

            text += f"{medal} <@{row[1]}>\nВремя: {int(days)}д {int(hours)}ч {int(minutes)}м\n\n"

        embed = disnake.Embed(description=text, colour=self.ProfileColor)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Leaders(bot))
