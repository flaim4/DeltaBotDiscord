import random
import disnake 

from typing import Dict
from utility.main import *
from disnake.ext import commands 

class Welcome(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self.welcome: load_json = load_json()

    def random_message(self, member: disnake.Member) -> disnake.Embed:
        message: Dict[str, str] = random.choice(self.welcome)
        embed: disnake.Embed = disnake.Embed(
            description = message['description'].format(name = member.name),
            colour = 0x2f3136
        ).set_image(url=message['image'])
        return embed

    @commands.Cog.listener()
    async def on_member_join(self, member: disnake.Member) -> None: 
        print_log(f"{member.name}, join in {member.guild.name}")
        embed: disnake.Embed = self.random_message(member)   
        channel: disnake.TextChannel = member.guild.get_channel(1291128236406734940)
        welcome_role: disnake.Role = member.guild.get_role(1165662641725919263)
        if welcome_role:
            await member.add_roles(welcome_role)
        if channel:
            await channel.send(embed=embed)
