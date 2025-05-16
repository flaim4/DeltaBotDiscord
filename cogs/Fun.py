import json
import os
import time
from collections import deque
from typing import Optional
import disnake
from disnake.ext import commands
import aiohttp
import requests
from disnake.ext.commands.context import AnyContext
import re
import asyncio
import util.ErrorHelper as ErrorHelper
from util._init_ import Indelifer

lock = asyncio.Lock()
pattern_member_ping = r"<@(\d+)>"
MAX_CALLS = 320
TIME_WINDOW = 300

call_times = deque()

def can_call():
    current_time = time.time()
    while call_times and current_time - call_times[0] > TIME_WINDOW:
        call_times.popleft()
    if len(call_times) < MAX_CALLS:
        return True, 0
    else:
        wait_time = TIME_WINDOW - (current_time - call_times[0])
        return False, wait_time

chage_nekosia = os.path.join(os.work_dir, "nekosia.tags.bak")
if os.path.exists(chage_nekosia):
    js = json.load(open(chage_nekosia, encoding="utf-8"))
else:
    req = requests.get("https://api.nekosia.cat/api/v1/tags")
    js = req.json()
    json.dump(js, open(chage_nekosia, encoding="utf-8", mode="w"))

chage_otakugifs = os.path.join(os.work_dir, "otakugifs.tags.bak")
if os.path.exists(chage_otakugifs):
    js2 = json.load(open(chage_otakugifs, encoding="utf-8"))
else:
    req = requests.get("https://api.otakugifs.xyz/gif/allreactions")
    js2 = req.json()
    json.dump(js2, open(chage_otakugifs, encoding="utf-8", mode="w"))



class OtakugifsBaseAction(commands.Converter):
    def __init__(self, action : str, format : str):
        self.action = action
        self.format = format
    async def convert(self, ctx: AnyContext, targets : str) -> disnake.Embed:
        try:
            match = re.search(pattern_member_ping, targets)
            if match:
                target = disnake.utils.get(ctx.guild.members, id=int(match.group(1)))
                if target is None:
                    return disnake.Embed(description="The user could not be found")
            else:
                target = disnake.utils.get(ctx.guild.members, name=targets)
                if target is None:
                    try:
                        target = disnake.utils.get(ctx.guild.members, id=int(targets))
                        if target is None:
                            return disnake.Embed(description="The user could not be found")
                    except:
                        return disnake.Embed(description="The user could not be found")
            async with lock:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"https://api.otakugifs.xyz/gif?reaction={self.action}&format=gif") as r:
                        if r.status == 200:
                            embed = disnake.Embed(description=self.format.format(ctx, target)).set_image(
                                (await r.json())["url"])
                            embed._footer = {
                                "text": "Powered by otakugifs.xyz",
                            }
                            return embed
                        return disnake.Embed().set_image(f"https://http.cat/{r.status}")
        except Exception as e:
            return disnake.Embed(description=f"A bot error occurred,\n error indelifer: {ErrorHelper.save_error_report(e, {'author': ctx.author.id, 'content': targets})}\ncontact the bot developers at [discord](<https://discord.gg/kJSWvqxtre>)")

class OtakugifsBase(commands.Converter):
    async def convert(self, ctx: AnyContext, action: str) -> Optional[str]:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.otakugifs.xyz/gif?reaction={action}&format=gif") as r:
                if r.status == 200:
                    return str((await r.json())["url"])
                return None



if js["status"] == 200:
    Tags = js["tags"]
    async def autocomp_tags(inter: disnake.ApplicationCommandInteraction, user_input: str):
        return [lang for lang in Tags if user_input.lower() in lang][:25]


    @Indelifer("fun")
    class Fun(commands.Cog):
        def __init__(self, bot):
            bot.add_cog(self)
            self.bot = bot

        @commands.slash_command()
        async def fun(self, ctx):
            pass

        @fun.sub_command()
        async def fox(self, ctx):
            async with lock:
                async with aiohttp.ClientSession() as session:
                    async with session.get("https://randomfox.ca/floof/") as r:
                        if r.status == 200:
                            embed = disnake.Embed(description="Random Fox").set_image((await r.json())["image"])
                            embed._footer = {
                                "text": "Powered by randomfox.ca",
                            }
                            await ctx.send(embed=embed)

        @fun.sub_command()
        async def dog(self, ctx):
            async with lock:
                async with aiohttp.ClientSession() as session:
                    async with session.get("https://random.dog/woof.json") as r:
                        if r.status == 200:
                            embed = disnake.Embed(description="Random Fox").set_image((await r.json())["url"])
                            embed._footer = {
                                "text": "Powered by random.dog",
                            }
                            await ctx.send(embed=embed)

        @fun.sub_command()
        async def anime(self, ctx, tag : str = commands.Param(autocomplete=autocomp_tags)):
            async with lock:
                can_call_result, wait_time = can_call()
                if can_call_result:
                    call_times.append(time.time())
                    async with aiohttp.ClientSession() as session:
                        async with session.get(f"https://api.nekosia.cat/api/v1/images/{tag}") as r:
                            if r.status == 200:
                                embed = disnake.Embed(description="Random Anime").set_image(
                                    (await r.json())["image"]["compressed"]["url"])
                                embed._footer = {
                                    "text": "Powered by nekosia.cat",
                                }
                                await ctx.send(embed=embed)
                else:
                    await ctx.send(f"Rate limit exceeded. Try again in {wait_time:.2f} seconds")


        @commands.command()
        async def airkiss(self, ctx, target: OtakugifsBaseAction("airkiss", "<@{0.author.id}> sends an air kiss to <@{1.id}>") = None):
            if target is None:
                await ctx.send(embed=disnake.Embed(title="Missing Argument",
                                                   description=f"The `member` argument is required.\nUsage: `{self.bot.command_prefix}{self.airkiss.name} <member>`"))
            else:
                await ctx.send(embed=target)

        @commands.command()
        async def kiss(self, ctx, target: OtakugifsBaseAction("kiss", "<@{0.author.id}> kisses  <@{1.id}>") = None):
            if target is None:
                await ctx.send(embed=disnake.Embed(title="Missing Argument",
                                                   description=f"The `member` argument is required.\nUsage: `{self.bot.command_prefix}{self.kiss.name} <member>`"))
            else:
                await ctx.send(embed=target)

        @commands.command()
        async def shout(self, ctx, target: OtakugifsBaseAction("shout", "<@{0.author.id}> shouts at <@{1.id}>") = None):
            if target is None:
                await ctx.send(embed=disnake.Embed(title="Missing Argument",
                                                   description=f"The `member` argument is required.\nUsage: `{self.bot.command_prefix}{self.shout.name} <member>`"))
            else:
                await ctx.send(embed=target)

        @commands.command()
        async def hug(self, ctx, target: OtakugifsBaseAction("hug", "<@{0.author.id}> hugs <@{1.id}>") = None):
            if target is None:
                await ctx.send(embed=disnake.Embed(title="Missing Argument",
                                                   description=f"The `member` argument is required.\nUsage: `{self.bot.command_prefix}{self.hug.name} <member>`"))
            else:
                await ctx.send(embed=target)

        @commands.command()
        async def slap(self, ctx, target: OtakugifsBaseAction("slap", "<@{0.author.id}> slaps <@{1.id}>") = None):
            if target is None:
                await ctx.send(embed=disnake.Embed(title="Missing Argument",
                                                   description=f"The `member` argument is required.\nUsage: `{self.bot.command_prefix}{self.slap.name} <member>`"))
            else:
                await ctx.send(embed=target)

        @commands.command()
        async def pat(self, ctx, target: OtakugifsBaseAction("pat", "<@{0.author.id}> slaps <@{1.id}>") = None):
            if target is None:
                await ctx.send(embed=disnake.Embed(title="Missing Argument",
                                                   description=f"The `member` argument is required.\nUsage: `{self.bot.command_prefix}{self.pat.name} <member>`"))
            else:
                await ctx.send(embed=target)

        @commands.command()
        async def cuddle(self, ctx, target: OtakugifsBaseAction("cuddle", "<@{0.author.id}> embraces <@{1.id}>") = None):
            if target is None:
                await ctx.send(embed=disnake.Embed(title="Missing Argument",
                                                   description=f"The `member` argument is required.\nUsage: `{self.bot.command_prefix}{self.pat.name} <member>`"))
            else:
                await ctx.send(embed=target)

        @commands.command()
        async def cry(self, ctx, target: OtakugifsBaseAction("cry", "<@{1.id}> made <@{0.author.id}> sad! :C") = None):
            if target is None:
                embed = disnake.Embed(description=f"<@{ctx.author.id}> is sad :C").set_image(await OtakugifsBase().convert(ctx, "cry"))
                embed._footer = {
                    "text": "Powered by otakugifs.xyz",
                }
                await ctx.send(embed=embed)
            else:
                await ctx.send(embed=target)