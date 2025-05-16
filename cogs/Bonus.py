from disnake.ext import commands
from util.balance import *
from util.TimeOut import *
import asyncio
lock = asyncio.Lock()
from disnake.interactions.application_command import ApplicationCommandInteraction
import random
import time
import json
from numba import njit
import numpy as np
from util._init_ import Indelifer

@njit
def random(prev_vals, window_size):
    r = np.random.randint(1, 500)
    n = len(prev_vals)
    if n < window_size:
        vals = np.empty(n + 1, dtype=np.float64)
        for i in range(n):
            vals[i] = prev_vals[i]
        vals[-1] = r
    else:
        vals = np.empty(window_size, dtype=np.float64)
        for i in range(1, window_size):
            vals[i - 1] = prev_vals[i]
        vals[-1] = r
    return vals, np.mean(vals)


vals = np.empty(0)

@Indelifer("bonus")
class Bonus(commands.Cog):
    @commands.slash_command()
    async def bonus(self, ctx: ApplicationCommandInteraction):
        async with lock:
            global vals
            server_id = ctx.guild.id
            user_id = ctx.author.id
            
            timeout_info = TimeOut.getTimeOut(server_id, user_id)
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
            
            vals, bonus_amount = random(vals,window_size=5)
            Balance.addBalance(server_id, user_id, bonus_amount)
            
            TimeOut.updateTimeOut(server_id, user_id, json.dumps({"bonus": current_time}))
            await ctx.send(f"Поздравляем! Вы получили бонус: {bonus_amount} монет.")