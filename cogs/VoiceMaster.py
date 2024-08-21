import disnake
import sqlite3
from util.db import Data

from disnake.ext import commands
    

class voiceMaster(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cur = Data.getCur()
        

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):

        cur = self.cur
        if before.channel is None and after.channel is not None:
            if (after.channel.id == 1207780991767158834):
                with Data.getCur() in cur:

                    guild : disnake.Guild = member.guild

                    category = disnake.utils.get(guild.categories, id = 1207780191167058020)

                    await guild.create_voice_channel(name = str(member.global_name), category = category)
                    cur.execute("""SELECT * FROM VoiceMaster WHERE server_id = ? AND user_id = ?", (server_id, user_id)""")
                    row = cur.fetchone()
                    if (row):
                        pass
                    else: 
                        pass



        elif before.channel is not None and after.channel is None:
            pass

def setup(bot):
    bot.add_cog(voiceMaster(bot))