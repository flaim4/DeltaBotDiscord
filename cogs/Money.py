import disnake
import time
import random
from disnake.ext import commands
from util.ManagerTime import ManagerTime  # Если этот модуль ваш, проверьте корректность пути
from util.balance import Balance  # Если этот модуль ваш, проверьте корректность пути

from disnake.interactions.application_command import ApplicationCommandInteraction

class Money(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.heshmap = {}  # Инициализируем хешмап как часть объекта

    @commands.slash_command()
    async def day(self, ctx: ApplicationCommandInteraction):
        # Проверяем наличие ключа для пользователя в словаре
        if ctx.author.id in self.heshmap:
            # Проверяем, истек ли таймер
            if time.time() > self.heshmap[ctx.author.id]["timeOut"]:
                # Генерируем случайное число в диапазоне от 50 до 150
                reward = random.randint(50, 150)
                
                # Добавляем баланс пользователю
                res: Balance = Balance.addBalance(ctx.guild.id, ctx.author.id, reward)
                
                await ctx.send(f"Вы получили награду: {reward}. Ваш новый баланс: {res}", ephemeral=True)
                
                # Обновляем таймер
                self.heshmap[ctx.author.id]["timeOut"] = time.time() + 18000  # 5 часов (в секундах)
            else: 
                await ctx.send("Вы уже забирали награду, возвращайтесь позже.", ephemeral=True)
        else:
            # Если ключа нет, создаем его и добавляем награду
            reward = random.randint(50, 150)
            res: Balance = Balance.addBalance(ctx.guild.id, ctx.author.id, reward)
            
            self.heshmap[ctx.author.id] = {
                "timeOut": time.time() + 18000  # Устанавливаем таймер на 5 часов
            }
            await ctx.send(f"Вы получили свою первую награду: {reward}. Ваш новый баланс: {res}", ephemeral=True)

def setup(bot):
    bot.add_cog(Money(bot))
