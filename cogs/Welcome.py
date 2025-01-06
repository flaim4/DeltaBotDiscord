import disnake
from disnake.ext import commands
import random
import settings

ProfileColor = settings.InvisibleColor

class Welcome(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.gif_links = [
            "https://media1.tenor.com/m/gfeo4ibN2LsAAAAC/taiga-toradora.gif",
            "https://media1.tenor.com/m/g0QIOyhPLRQAAAAC/neon_cove-cute.gif",
            "https://media1.tenor.com/m/FIlCOtD3tdwAAAAC/anime-catgirl.gif",
            "https://media1.tenor.com/m/G3WsQADueVEAAAAC/sistine-neko.gif",
            "https://media.tenor.com/your-choice.gif",
            "https://media.tenor.com/another-choice.gif",
            "https://media.tenor.com/some-welcome-gif.gif"
        ]
        self.welcome_messages = [
            "Привет, {member_mention}! Мы так рады, что ты с нами!  Загляни в каналы и начни общаться! ",
            "Добро пожаловать, {member_mention}!  Ты попал в замечательное место! Наслаждайся общением и дружбой! ",
            "Эй, {member_mention}, добро пожаловать на сервер!  Мы уверены, что тебе тут понравится! ",
            "Привет, {member_mention}! Мы рады, что ты с нами!  Присоединяйся к обсуждениям и не забывай веселиться! "
        ]

    def randomMessage(self, member: disnake.Member) -> disnake.Embed:
        random_message = random.choice(self.welcome_messages).format(member_mention=member.mention)
        embed = disnake.Embed(
            title=f"✨ Добро пожаловать, {member.name}! ✨",
            description=(
                f"{random_message}\n\n"
                "Не забудь прочитать правила и настроить профиль. 😉"
            ),
            colour=0x2b2d31
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_image(url=random.choice(self.gif_links))
        embed.set_footer(
            text="Мы надеемся, что тебе здесь понравится!",
            icon_url=self.bot.user.display_avatar.url
        )
        return embed
    
    @commands.slash_command()
    async def test_invite(self, inter: disnake.ApplicationCommandInteraction):
        random_message = random.choice(self.welcome_messages).format(member_mention=inter.user.mention)
        embed = disnake.Embed(
            title="Добро пожаловать на сервер!",
            description=(
                f"{random_message}\n\n"
                "Не забудь прочитать правила. 😉"
            ),
            colour=0x2b2d31
        )
        embed.set_thumbnail(url=inter.user.display_avatar.url)
        embed.set_image(url=random.choice(self.gif_links))
        embed.set_footer(
            text="Мы надеемся, что тебе здесь понравится!",
            icon_url=self.bot.user.display_avatar.url
        )

        await inter.response.send_message(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member: disnake.Member):
        
        channel = member.guild.get_channel(1222841123597324370)
        welcome_role = member.guild.get_role(1208444981849620642)

        if welcome_role:
            await member.add_roles(welcome_role, reason="Приветственная роль")

        if channel:
            embed = self.randomMessage(member)
            await channel.send(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(Welcome(bot))
