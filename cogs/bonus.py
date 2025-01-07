from disnake.ext import commands

from util.balance import *
from util.TimeOut import *

from disnake.interactions.application_command import ApplicationCommandInteraction

import random
import time
import json

class Bonus(commands.Cog):
    @commands.slash_command()
    async def bonus(self, ctx: ApplicationCommandInteraction):
        server_id = ctx.guild.id
        user_id = ctx.author.id

        timeout_info = TimeOut.getTimeOut(server_id, user_id)
        current_time = time.time()

        if timeout_info:
            timeout_data = json.loads(timeout_info)
            last_bonus_time = int(timeout_data.get("bonus", 0))

            if current_time - last_bonus_time < 86400:
                remaining_time = 86400 - (current_time - last_bonus_time)
                hours = int(remaining_time // 3600)
                minutes = int((remaining_time % 3600) // 60)
                seconds = int(remaining_time % 60)
                await ctx.send(f"Вы уже получили бонус. Попробуйте снова через {hours}ч {minutes}м {seconds}с.")
                return

        bonus_amount = random.randint(1, 500)
        Balance.addBalance(server_id, user_id, bonus_amount)

        TimeOut.updateTimeOut(server_id, user_id, json.dumps({"bonus": current_time}))

        await ctx.send(f"Поздравляем! Вы получили бонус: {bonus_amount} монет.")

def setup(bot):
    bot.add_cog(Bonus(bot))



def setup(bot):
    bot.add_cog(Bonus(bot))