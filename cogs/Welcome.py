import disnake
from disnake.ext import commands
import random
import settings
import util.Resouces as res
from random import Random

ProfileColor = settings.InvisibleColor
random = Random(0)


class Welcome(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.metadata = res.loadJson("welcome")

    def randomMessage(self, member: disnake.Member, channel) -> disnake.Embed:
        embed = disnake.Embed(
            title=f"✨ Добро пожаловать, {member.name}! ✨",
            description=(
                f"{str(self.metadata['dist']["text"][random.randrange(0, len(self.metadata['dist']["text"]))]).format(member, channel, disnake.guild.Guild)}\n\n"
                "Не забудь прочитать правила и настроить профиль. 😉"
            ),
            colour=0x2b2d31
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_image(url=self.metadata['dist']["image"][random.randrange(0, len(self.metadata['dist']["image"]))])
        embed.set_footer(
            text="Мы надеемся, что тебе здесь понравится!",
            icon_url=self.bot.user.display_avatar.url
        )
        return embed

    @commands.slash_command(default_member_permissions=disnake.Permissions(administrator=True))
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
        embed.set_thumbnail(url=inter.author.avatar.url if inter.author.avatar else inter.author.default_avatar.url)
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
            await member.add_roles(welcome_role)

        if channel:
            embed = self.randomMessage(member, channel)
            await channel.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Welcome(bot))
