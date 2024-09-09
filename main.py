from disnake.ext import commands
from dotenv import load_dotenv
import sqlite3
import disnake 
import os

from util.db import Data



bot = commands.Bot(command_prefix="-", intents=disnake.Intents.all())
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


cur = Data.getCur()

@bot.event
async def on_ready():
	await bot.change_presence(status=disnake.Status.online, activity=disnake.Activity(type=disnake.ActivityType.watching, name="DOORS 2", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"))#Not started
	print('Successful login in:', bot.user)

for filename in os.listdir('./cogs'):
    if filename.endswith('.cls.py'):

        with open(f"./cogs/{filename}", 'r', encoding='utf-8') as file:
           namespace = {}
           exec(file.read(), namespace)

           class_dict = {name: obj for name, obj in namespace.items() if isinstance(obj, type)}
           if filename[:-7] in class_dict:
               class_dict[filename[:-7]](bot)
               continue
        
        
                
    if filename.endswith('.py'):
        if (filename == "_init_.py"):
            continue
        print(filename)
        bot.load_extension(f'cogs.{filename[:-3]}')

token = os.getenv('TOKEN')
bot.run(token)
