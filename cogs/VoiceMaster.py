import disnake
import sqlite3
from util.db import *
from disnake.ext import commands
    

class voiceMaster(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cur = Data.getCur()
        

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel is None and after.channel is not None:
            if (after.channel.id == 1207780991767158834):
                pass
            

        elif before.channel is not None and after.channel is None:
            pass

def setup(bot):
    bot.add_cog(voiceMaster(bot))