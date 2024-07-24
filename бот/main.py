from disnake.ext import commands
from dotenv import load_dotenv
import sqlite3
import disnake 
import os

bot = commands.Bot(command_prefix="-", intents=disnake.Intents.all())

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

conn = sqlite3.connect("data.db")
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS users(server_id INTEGER, user_id INTEGER, lvl INTEGER DEFAULT 1, xp INTEGER DEFAULT 0, money INTEGER DEFAULT 0)""")

@bot.event
async def on_ready():
	await bot.change_presence(status=disnake.Status.online, activity=disnake.Activity(type=disnake.ActivityType.watching, name="Not started"))
	print('Successful login in:', bot.user)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        if (filename == "_init_.py"):
            continue
        print(filename)
        bot.load_extension(f'cogs.{filename[:-3]}')

token = os.getenv('TOKEN')
bot.run(token)