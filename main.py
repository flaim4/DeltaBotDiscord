import os
import disnake
from cogs import load_cogs
from utility.main import *
from utility.db_init import *
from dotenv import load_dotenv
from disnake.ext import commands

bot: commands.Bot = commands.Bot(command_prefix = "?", intents = disnake.Intents.all())

db_init()
load_cogs(bot)

dotenv_path: os.path.join = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

@bot.event
async def on_ready() -> None:
    print_log(f"The bot {bot.user.name} is started.")

bot.run(os.getenv('TOKEN'))