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
            disnake.Embed(description=f"### Добро пожаловать на сервер! 🚀\n Приветствуем тебя в нашем сообществе, {member.global_name}! Пожелаем удачи и надеемся на интересное общение.", color=ProfileColor)
                .set_thumbnail(url=member.avatar.url)
                .set_image(url="https://cdn.discordapp.com/attachments/1071030207726755882/1216159185767497828/graund.png"),
            disnake.Embed(description=f"### Приветствуем нового участника! ✨\n Добро пожаловать на наш сервер, {member.global_name}! Пусть здесь тебе будет комфортно. Удачи и приятного времяпрепровождения!", color=ProfileColor)
                .set_thumbnail(url=member.avatar.url)
                .set_image(url="https://cdn.discordapp.com/attachments/1071030207726755882/1216159185767497828/graund.png"),
            disnake.Embed(description=f"### Добро пожаловать в нашу дружную команду! 🌈\n Счастливы видеть нового участника, {member.global_name}! Надеемся, ты найдешь здесь много интересного. Удачи и хорошего настроения!", color=ProfileColor)
                .set_thumbnail(url=member.avatar.url)
                .set_image(url="https://cdn.discordapp.com/attachments/1071030207726755882/1216159185767497828/graund.png"),
            disnake.Embed(description=f"### Приветствуем нового участника! 🌟\n Добро пожаловать на наш сервер, {member.global_name}! Надеемся, тебе здесь понравится. Удачи и приятного общения!", color=ProfileColor)
                .set_thumbnail(url=member.avatar.url)
                .set_image(url="https://cdn.discordapp.com/attachments/1071030207726755882/1216159185767497828/graund.png")
        ]
        return Hesh[random.randint(0, 4)]

    @commands.Cog.listener()
    async def on_member_join(self, member: disnake.Member):
        if (member.bot):
            await member.ban()
        else:
            embed: disnake.Embed = self.randomMessage(member)
            channel: disnake.guild.GuildChannel = member.guild.get_channel(1222841123597324370)
            welcomeRole: disnake.Role = member.guild.get_role(1208444981849620642)
            if (welcomeRole):
                await member.add_roles(welcomeRole)
            if channel:
                await channel.send(embed=embed)

def setup(bot: commands.Bot): 
    bot.add_cog(Welcome(bot))
