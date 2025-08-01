from disnake.ext import commands
from util.balance import *
from util.TimeOut import *
import asyncio
lock = asyncio.Lock()
from disnake.interactions.application_command import ApplicationCommandInteraction
import random
import time
import json
from util._init_ import Indelifer, CogBase


@Indelifer("bonus")
class Bonus(CogBase):

    @commands.slash_command()
    async def bonus(self, ctx: ApplicationCommandInteraction):
        async with Data.timeOut as timeout:
            global vals
            server_id = ctx.guild.id
            user_id = ctx.author.id

            result = timeout.execute(
                "SELECT json FROM TimeOut WHERE server_id = ? AND user_id = ?",
                (server_id, user_id)
            ).fetchone()
            timeout_info = result[0] if result else None
            
            current_time = time.time()
            
            if not (timeout_info == None):
                timeout_data = json.loads(timeout_info)
                last_bonus_time = int(timeout_data.get("bonus", 0))
                if current_time < (last_bonus_time + 86400):
                    remaining_time = 86400 - (current_time - last_bonus_time)
                    hours = int(remaining_time // 3600)
                    minutes = int((remaining_time % 3600) // 60)
                    seconds = int(remaining_time % 60)
                    await ctx.send(f"Вы уже получили бонус. Попробуйте снова через {hours}ч {minutes}м {seconds}с.")
                    return
            
            bonus_amount = random.randint(50, 500)
            await Balance.addBalance(server_id, user_id, bonus_amount)

            timeout.execute(
                """INSERT INTO TimeOut (server_id, user_id, json)
                    VALUES (?, ?, ?)
                    ON CONFLICT(server_id, user_id) DO UPDATE SET json = excluded.json""",
                (server_id, user_id, json.dumps({"bonus": current_time}))
            )
            await timeout.commit()
            await ctx.send(f"Поздравляем! Вы получили бонус: {bonus_amount} монет.")