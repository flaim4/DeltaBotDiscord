import disnake 
from disnake import Embed

from disnake.ext import commands 

from disnake.ext.commands import Context
from disnake import Message
from disnake.abc import Messageable

from disnake.interactions.application_command import ApplicationCommandInteraction

from enum import Enum

import random
import asyncio

class Entry(Enum):
    watermelon = ':watermelon:'
    lemon = ':lemon:'
    tangerine = ':tangerine:'
    banana = ':banana:'

def find_triples(matrix):
    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0
    triples = []

    for r in range(rows):
        for c in range(cols - 2):
            if matrix[r][c] == matrix[r][c + 1] == matrix[r][c + 2]:
                triples.append(matrix[r][c])
    
    for c in range(cols):
        for r in range(rows - 2):
            if matrix[r][c] == matrix[r + 1][c] == matrix[r + 2][c]:
                triples.append(matrix[r][c])

    for r in range(rows - 2):
        for c in range(cols - 2):
            if matrix[r][c] == matrix[r + 1][c + 1] == matrix[r + 2][c + 2]:
                triples.append(matrix[r][c])

    for r in range(rows - 2):
        for c in range(2, cols):
            if matrix[r][c] == matrix[r + 1][c - 1] == matrix[r + 2][c - 2]:
                triples.append( matrix[r][c])

    return triples

def weighted_choice(choices, weights):
    total = sum(weights)
    r = random.uniform(0, total)
    upto = 0
    for choice, weight in zip(choices, weights):
        if upto + weight >= r:
            return choice
        upto += weight

def generate_row(length, enum_values):
    row = []
    for i in range(length):
        choices = list(enum_values)
        weights = [1] * len(choices)

        if i >= 2 and row[-1] == row[-2]:
            last_value_index = choices.index(row[-1])
            weights[last_value_index] = 0.1

        row.append(weighted_choice(choices, weights))
    return row

class Balance(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        bot.add_cog(self)
        
    @commands.default_member_permissions(administrator=True)
    @commands.command()
    async def kz(self, ctx : ApplicationCommandInteraction, money: int = 100):
        coins = money
        array = [generate_row(3, list(Entry)) for _ in range(6)]

        msg = await ctx.channel.send(embed=Embed(title=f"Ставка: {coins}:Nigers", description=f"Starting.."))
       
        for i in range(1, len(array) - 1):
            await msg.edit(embed=Embed(title=f"Ставка: {coins}:Nigers", description=f"{' '.join([entry.value for entry in array[i-1]])}\n{' '.join([entry.value for entry in array[i]])}\n{' '.join([entry.value for entry in array[i+1]])}")) 
            await asyncio.sleep(0.1)

        end = [
            array[len(array) - 3],
            array[len(array) - 2],
            array[len(array) - 1]
        ]

        kl = find_triples(end)

        if (len(kl) > 0):
            for ik in kl:
                if (ik == Entry.lemon):
                    coins += 10
                elif (ik == Entry.banana):
                    coins += 12
                elif (ik == Entry.tangerine):
                    coins += 14
                elif (ik == Entry.watermelon):
                    coins += 16
        else:
            coins = 0
            pass

        await msg.edit(embed=Embed(title=f"Ставка: {coins}:Nigers", description=f"{' '.join([entry.value for entry in array[len(array) - 3]])}\n{' '.join([entry.value for entry in array[len(array) - 2]])}\n{' '.join([entry.value for entry in array[len(array) - 1]])}").set_footer(text=f"Виграш: {coins}"))

    @commands.command()
    async def ah_user(self, ctx : ApplicationCommandInteraction, stavka: int = 100, member : disnake.Member = None): 
        msg = await ctx.channel.send(embed=Embed(title=f"Ставка: {coins}:Nigers", description=f"Starting.."))
        pass

