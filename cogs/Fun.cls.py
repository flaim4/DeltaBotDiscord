#https://randomfox.ca/floof/
#https://random.dog/woof.json
from typing import Union, Callable

import disnake
from disnake.ext import commands
from disnake.interactions.application_command import ApplicationCommandInteraction
import util.Resouces as res
import aiohttp


class Fun(commands.Cog):
    def __init__(self, bot):
        bot.add_cog(self)
        self.bot = bot

    @commands.slash_command()
    async def fun(self, ctx):
       pass

    @fun.sub_command()
    async def fox(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://randomfox.ca/floof/") as r:
                if r.status == 200:
                    embed = disnake.Embed(description="Random Fox").set_image((await r.json())["image"])
                    embed._footer = {
                        "text": "https://randomfox.ca/floof/",
                    }
                    await ctx.send(embed=embed)

    @fun.sub_command()
    async def dog(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://random.dog/woof.json") as r:
                if r.status == 200:
                    embed = disnake.Embed(description="Random Fox").set_image((await r.json())["url"])
                    embed._footer = {
                        "text": "https://random.dog/",
                    }
                    await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Fun(bot))