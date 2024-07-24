import disnake 
from disnake.ext import commands


class ошибки(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Лист ошибок")
    async def ошибки(self, ctx):
        embed = disnake.Embed(description="**Ошибка 105**: Означает что команда в __кулдауне__\n**Ошибка 404**: Команда не __работает__ или в __разработке__\n**Ошибка 267**: Означает что у вас недостаточно прав для использования команды",
                      colour=0x2b2d31)

        embed.set_author(name="Ghost World",
                 url="https://discord.gg/FRy9B3cn5f",
                 icon_url="https://cdn.discordapp.com/attachments/1151924278074298398/1173700533912096918/Frame_5_8.png?ex=6564e8cd&is=655273cd&hm=f27d7cf429fadb7be6b2bd6e6717346f759a6a64e77a4068c1f1a1adcbd44e70&")

        await ctx.send(embed=embed, ephemeral=True)

    def cog_unload(self):
        self.conn.close()

def setup(bot):
    bot.add_cog(ошибки(bot))
