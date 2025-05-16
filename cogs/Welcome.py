import disnake
from disnake.ext import commands
import random
import settings
import util.Resouces as res
from random import Random
from util._init_ import Indelifer

ProfileColor = settings.InvisibleColor
random = Random(0)

@Indelifer("welcome")
class Welcome(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.metadata = res.loadYaml("welcome")

    def randomMessage(self, member: disnake.Member, channel) -> disnake.Embed:
        member.name
        embed = disnake.Embed(
            title=self.metadata["title"][random.randrange(0, len(self.metadata["title"]))].format(member, channel, disnake.guild.Guild),
            description=(
                f"{str(self.metadata["text"][random.randrange(0, len(self.metadata["text"]))]).format(member, channel, disnake.guild.Guild)}\n\n"
                "Не забудь прочитать правила и настроить профиль. 😉"
            ),
            colour=0x2b2d31
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_image(url=self.metadata["image"][random.randrange(0, len(self.metadata["image"]))])
        embed.set_footer(
            text="Мы надеемся, что тебе здесь понравится!",
            icon_url=self.bot.user.display_avatar.url
        )
        return embed

    @commands.slash_command(default_member_permissions=disnake.Permissions(administrator=True))
    async def test_invite(self, inter: disnake.ApplicationCommandInteraction):

        await inter.response.send_message(embed=self.randomMessage(inter.author, inter.channel))

    @commands.Cog.listener()
    async def on_member_join(self, member: disnake.Member):

        channel = member.guild.get_channel(1222841123597324370)
        welcome_role = member.guild.get_role(1208444981849620642)

        if welcome_role:
            await member.add_roles(welcome_role)

        if channel:
            embed = self.randomMessage(member, channel)
            await channel.send(embed=embed)