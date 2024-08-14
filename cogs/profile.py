import disnake 
from disnake.ext import commands
from disnake import TextInputStyle
import sqlite3
import time
import settings
from disnake import colour
from util.member import Member
from util.balance import Balance

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Отображает профиль пользователя.")
    async def profile(self, ctx, member: disnake.Member = None):
        
        if ctx.author.bot:
            return
        
        # Если member не указан, установить его на ctx.author
        if member is None:
            member = ctx.author

        # Проверка на то, является ли member ботом
        if member.bot:
            await ctx.send("Я не могу посмотреть профиль бота.", ephemeral=True)
            return
        
        # Отображение профиля пользователя
        name=member.display_name
        server = ctx.guild

        voice_seconds = Member.getCountSecondVoice(member.guild.id, member.id)

        # Обработка случая, если voice_seconds None или нулевой
        if voice_seconds is None or voice_seconds == 0:
            days, hours, minutes, seconds = 0, 0, 0, 0
        else:
            days, hours, minutes, seconds = Member.convert_seconds(voice_seconds)

        ProfileColor = settings.InvisibleColor
        ErrorColor = settings.ErrorColor
        if server.icon is None:

            embed = disnake.Embed(description=f"> **Основная информация**\n```Имя пользователя: {name}\nО себе: Beta\nКлан: Beta```",colour=ProfileColor)

            embed.set_author(name=f"{name} • Профиль", icon_url=member.avatar)
            
            embed.add_field(name="> Уровень", value="```yaml\n1```", inline=True)
            embed.add_field(name="> Опыт", value="```yaml\n2```", inline=True)
            embed.add_field(name="> Баланс", value=f"```yaml\n{Balance.getBalance(member.guild.id, member.id)}```", inline=True)
            embed.add_field(name="> Активность", value=f"```yaml\n{days}д {hours}ч {minutes}м {seconds}с```", inline=True)
            embed.add_field(name="> Сообщения", value=f"```yaml\n{Member.getCountMessage(member.guild.id, member.id)}```", inline=True)
            
            await ctx.send(embed=embed)
        else:
            embed = disnake.Embed(description=f"> **Основная информация**\n```Имя пользователя: {name}\nО себе: Beta\nКлан: Beta```", colour=ProfileColor)
            
            embed.set_author(name=f"{name} • Профиль", icon_url=member.avatar)
    
            embed.add_field(name="> Уровень", value="```yaml\n1```", inline=True)
            embed.add_field(name="> Опыт", value="```yaml\n2```", inline=True)
            embed.add_field(name="> Баланс", value=f"```yaml\n{Balance.getBalance(member.guild.id, member.id)}```", inline=True)
            embed.add_field(name="> Нарушения", value="```yaml\n4```", inline=True)
            embed.add_field(name="> Активность", value=f"```yaml\n{int(days)}д {int(hours)}ч {int(minutes)}м```", inline=True)
            embed.add_field(name="> Сообщения", value=f"```yaml\n{Member.getCountMessage(member.guild.id, member.id)}```", inline=True)
            
            await ctx.send(embed=embed) 

    @commands.slash_command(description="Посмотреть")
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

def setup(bot):
    bot.add_cog(Profile(bot))