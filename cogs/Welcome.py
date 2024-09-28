import disnake
from disnake.ext import commands
import random
import settings

ProfileColor = settings.InvisibleColor

from disnake.interactions.application_command import ApplicationCommandInteraction

class Welcome(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    def randomMessage(self, member: disnake.Member) -> disnake.Embed:
        Hesh = [
            disnake.Embed(description=f"## {member.name} | Добро пожаловать.", colour=0x2f3136)
                .set_image(url="https://media1.tenor.com/m/gfeo4ibN2LsAAAAC/taiga-toradora.gif"),
            disnake.Embed(description=f"## {member.name} | Отлично, что ты с нами.", colour=0x2f3136)
                .set_image(url="https://media1.tenor.com/m/g0QIOyhPLRQAAAAC/neon_cove-cute.gif"),
            disnake.Embed(description=f"## {member.name} | Классно, что ты с нами.", colour=0x2f3136)
                .set_image(url="https://media1.tenor.com/m/FIlCOtD3tdwAAAAC/anime-catgirl.gif"),
            disnake.Embed(description=f"## {member.name} | Приветствуем тебя.", colour=0x2f3136)
                .set_image(url="https://media1.tenor.com/m/G3WsQADueVEAAAAC/sistine-neko.gif")
        ]
        return Hesh[random.randint(0, 3)]

    @commands.Cog.listener()
    async def on_member_join(self, member: disnake.Member):
        if (member.bot):
            await member.ban()
        else:
            embed: disnake.Embed = self.randomMessage(member)   
            channel: disnake.guild.GuildChannel = await member.guild.get_channel(1222841123597324370)
            welcomeRole: disnake.Role = await member.guild.get_role(1208444981849620642)
            if (welcomeRole):
                await member.add_roles(welcomeRole)
            if channel:
                await channel.send(embed=embed)

def setup(bot: commands.Bot): 
    bot.add_cog(Welcome(bot))
