import disnake 
from disnake.ext import commands

class informat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Отображает профиль пользователя.")
    async def информация(self, ctx, author: disnake.Member = None):
        if ctx.author.bot:
            return

        if author is None:
            author = ctx.author
        
        embed = disnake.Embed(title="Основная информация",
                      description=f"**Имя пользователя:** {author.display_name} ({author})\n**Статус:** NONE\n**Присоеденился:** дата1 (дата2)\n**Дата регистрации:** дата3 (дата4)")
        embed.set_author(name=f"Информация о {author.display_name}",
                         icon_url=author.avatar)
        embed.set_thumbnail(url=author.avatar)
        embed.set_footer(text=f"ID: {author.id}")

        await ctx.send(embed=embed)
      



def setup(bot):
    bot.add_cog(informat(bot))