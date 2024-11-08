import disnake 

from member.balance import Balance
from disnake.ext import commands

from disnake.interactions.application_command import ApplicationCommandInteraction

class Balance_commands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        bot: commands.Bot = bot

    @commands.slash_command()
    async def balance(ctx: ApplicationCommandInteraction):
        await ctx.send(Balance.get_balance(ctx.author))