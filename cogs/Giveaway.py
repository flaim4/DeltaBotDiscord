import disnake
import random
from disnake.ext import commands
from util._init_ import Indelifer, CogBase

@Indelifer("giveaway")
class Giveaway(CogBase):
    async def init(self):
        pass

    @commands.slash_command()
    async def giveaway(self, ctx: disnake.ApplicationCommandInteraction, duration: str):
        pass