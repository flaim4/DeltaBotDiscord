import disnake 
from disnake.ext import commands
from disnake import TextInputStyle
import sqlite3
import time
import settings
from datetime import datetime
from disnake import colour
from util.member import Member
from util.balance import Balance

from util.db import Data

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description=Data.lang.get("profile.description"))
    async def profile(self, ctx, member: disnake.Member = None):
        
        if ctx.author.bot:
            return
        
        if member is None:
            member = ctx.author

        if member.bot:
            await ctx.send(Data.lang.get("profile.botr"), ephemeral=True)
            return
        
        if (Member.getLoveMember(member.guild.id, member.id) is None):
            components = [disnake.ui.Button(label="Открыть любовный профиль", style=disnake.ButtonStyle.blurple, custom_id="love", disabled=True)]
        else:
            components = [disnake.ui.Button(label="Открыть любовный профиль", style=disnake.ButtonStyle.blurple, custom_id="love", disabled=False)]

        name=member.display_name
        server = ctx.guild

        voice_seconds = Member.getCountSecondVoice(member.guild.id, member.id)
        
        if voice_seconds is None or voice_seconds == 0:
            days, hours, minutes, seconds = 0, 0, 0, 0
        else:
            days, hours, minutes, seconds = Member.convert_seconds(voice_seconds)

        ProfileColor = settings.InvisibleColor
        ErrorColor = settings.ErrorColor
        
        embed = disnake.Embed(description=f"### Профиль — {member.global_name}", colour=ProfileColor)
        
        embed.add_field(name="> Уровень", value="```yaml\n1```", inline=True)
        embed.add_field(name="> Опыт", value="```yaml\n2```", inline=True)
        embed.add_field(name="> Баланс", value=f"```yaml\n{Balance.getBalance(member.guild.id, member.id)}```", inline=True)
        embed.add_field(name="> Нарушения", value=f"```yaml\n{Member.getWarns(member.guild.id, member.id)}```", inline=True)
        embed.add_field(name="> Активность", value=f"```yaml\n{int(days)}д {int(hours)}ч {int(minutes)}м```", inline=True)
        embed.add_field(name="> Сообщения", value=f"```yaml\n{Member.getCountMessage(member.guild.id, member.id)}```", inline=True)
        embed.set_thumbnail(url=member.avatar)
        await ctx.send(embed=embed, components=components) 


    @commands.slash_command(description=Data.lang.get("balance.description"))
    @commands.default_member_permissions(administrator=True)
    async def balance(self, ctx):
        await ctx.send(Balance.getBalance(ctx.guild.id, ctx.author.id))

    @commands.slash_command(description="Добавить баланс")
    @commands.default_member_permissions(administrator=True)
    async def addbalance(self, ctx, member: disnake.Member = None, count: int = 0):
        Balance.addBalance(ctx.guild.id, member.id, count)

    @commands.slash_command(description="Установить баланс")
    @commands.default_member_permissions(administrator=True)
    async def setbalance(self, ctx, member: disnake.Member = None, count: int = 0):
        Balance.setBalance(ctx.guild.id, member.id, count)

    @commands.slash_command(description="Забрать баланс")
    @commands.default_member_permissions(administrator=True)
    async def spendbalance(self, ctx, member: disnake.Member = None, count: int = 0):
        Balance.spendBalance(ctx.guild.id, member.id, count)


    @commands.Cog.listener(disnake.Event.button_click)
    async def button_click(self, inter: disnake.MessageInteraction):
        if (inter.component.custom_id == "love"):
            embed = disnake.Embed(description=f"### Любовный профиль — {inter.author.global_name}")
            love_member = inter.guild.get_member(Member.getLoveMember(inter.guild.id, inter.author.id))
            embed.add_field(name = "> Партнер", value = f"```{love_member.global_name}```", inline=False)
            current_datetime = datetime.fromtimestamp(Member.getLoveMemberDataRegister(inter.guild.id, inter.user))
            formatted_time = current_datetime.strftime('%Y-%m-%d')
            embed.add_field(name = "> Регистрация", value = f"```{formatted_time}```", inline=True)

            voice_seconds = time.time() - Member.getLoveMemberDataRegister(inter.guild.id, inter.user)
        
            if voice_seconds is None or voice_seconds == 0:
                days, hours, minutes, seconds = 0, 0, 0, 0
            else:
                days, hours, minutes, seconds = Member.convert_seconds(voice_seconds)

            embed.add_field(name = "> Всего вместе", value = f"```{int(days)}д {int(hours)}ч, {int(minutes)}м  ```", inline=True)
            embed.add_field(name = "> Времени проведено в любовной комнате", value = f"```{Member.getLoveMemberTimeVoice(inter.guild.id, inter.user)}```", inline=False)
            embed.set_thumbnail(url=inter.author.avatar.url)
            ProfileColor = settings.InvisibleColor
            embed.color = ProfileColor
            await inter.send(embed=embed)

def setup(bot):
    bot.add_cog(Profile(bot))