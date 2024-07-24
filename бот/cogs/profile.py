import disnake 
from disnake.ext import commands
from disnake import TextInputStyle
import sqlite3
import time
from util.balance import Balance
import settings
from disnake import colour
from util.member import Member

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

        #Цвет профиля
        ProfileColor = settings.InvisibleColor
        ErrorColor = settings.ErrorColor

        if server.icon is None:
            embed = disnake.Embed(description=f"> **Основная информация**\n```Имя пользователя: {name}\nО себе: Beta\nКлан: Beta```",colour=ProfileColor)

            embed.set_author(name=f"{name} • Профиль", icon_url=member.avatar)
            
            embed.add_field(name="> Уровень", value="```yaml\n1```", inline=True)
            embed.add_field(name="> Опыт", value="```yaml\n2```", inline=True)
            embed.add_field(name="> Баланс", value=f"```yaml\n{Balance.getBalance(member.guild.id, member.id)}```", inline=True)
            embed.add_field(name="> Нарушения", value="```yaml\n4```", inline=True)
            embed.add_field(name="> Активность", value="```yaml\n5```", inline=True)
            embed.add_field(name="> Сообщения", value=f"```yaml\n{Member.getCountMessage(member.guild.id, member.id)}```", inline=True)

            embed.set_footer(text=str(settings.MiniServerName))
            
            await ctx.send(embed=embed, components=[
                    disnake.ui.Button(
                        label="бим",
                        style=disnake.ButtonStyle.primary,
                        custom_id="bim"
                    ),
                    disnake.ui.Button(
                        label="🎁Бонус",
                        style=disnake.ButtonStyle.success,
                        custom_id="bonus"
                    )
                ])
        else:
            embed = disnake.Embed(description=f"> **Основная информация**\n```Имя пользователя: {name}\nО себе: Beta\nКлан: Beta```", colour=ProfileColor)
            
            embed.set_author(name=f"{name} • Профиль", icon_url=member.avatar)
    
            embed.add_field(name="> Уровень", value="```yaml\n1```", inline=True)
            embed.add_field(name="> Опыт", value="```yaml\n2```", inline=True)
            embed.add_field(name="> Баланс", value=f"```yaml\n{Balance.getBalance(member.guild.id, member.id)}```", inline=True)
            embed.add_field(name="> Нарушения", value="```yaml\n4```", inline=True)
            embed.add_field(name="> Активность", value="```yaml\n5```", inline=True)
            embed.add_field(name="> Сообщения", value=f"```yaml\n{Member.getCountMessage(member.guild.id, member.id)}```", inline=True)
            embed.set_footer(text=str(settings.MiniServerName), icon_url=server.icon)
            
            await ctx.send(embed=embed, components=[
                    disnake.ui.Button(
                        label="бим",
                        style=disnake.ButtonStyle.primary,
                        custom_id="bim"
                    ),
                    disnake.ui.Button(
                        label="🎁Бонус",
                        style=disnake.ButtonStyle.success,
                        custom_id="bonus"
                    )
                ])

    #@profile.error
    #async def profile_error(self, ctx, error):
    #    author = ctx.author
    #    name = ctx.author.display_name
    #    embed = disnake.Embed(description="Произошла ошибка попробуйте ещё раз.",
    #                   colour=ErrorColor)
    #    embed.set_author(name=f"{name} • Ошибка 404", icon_url=author.avatar)
    #    await ctx.send(embed=embed, ephemeral=True)

    @commands.slash_command(description="Посмотреть")
    @commands.default_member_permissions(administrator=True)
    async def balance(self, ctx):
        await ctx.send(Balance.getBalance(ctx.guild.id, ctx.author.id))

    @commands.slash_command(description="Добавить баланс")
    @commands.default_member_permissions(administrator=True)
    async def addbalance(self, ctx, member: disnake.Member = None, count: int = 0):
        Balance.addBalance(ctx.guild.id, member.id, count)

def setup(bot):
    bot.add_cog(Profile(bot))