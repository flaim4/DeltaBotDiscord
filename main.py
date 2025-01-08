from disnake.ext import commands
from dotenv import load_dotenv
import importlib.util
import disnake 
import os
import sys
import json
from util.db import Data
import util.Resouces as res
meta = res.loadJsonObject("base")

def loadenv():
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
        return True

    dotenv_path = os.path.join(os.path.dirname(__file__), "data", '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
        return True

    dotenv_path = os.path.join(os.path.dirname(__file__), ".venv", '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
        return True


bot = commands.Bot(command_prefix=meta.command_prefix,intents=disnake.Intents.all())
if not loadenv():
    sys.exit("Could not find Env file!")

cur = Data.getCur()

@bot.event
async def on_ready():
    await bot.change_presence(status=disnake.Status.online, activity=disnake.Activity(type=disnake.ActivityType.watching, name="DOORS 2", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"))#Not started
    print('Successful login in:', bot.user)


for filename in os.listdir('./cogs'):
    if filename.endswith('.cls.py'):
        file_path = os.path.join('./cogs', filename)

        spec = importlib.util.spec_from_file_location(filename[:-3], file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        class_dict = {name: obj for name, obj in vars(module).items() if isinstance(obj, type)}
        if filename[:-7] in class_dict:
            class_dict[filename[:-7]](bot)
            continue

    elif filename.endswith('.py') and filename != "_init_.py":
        module_name = f'cogs.{filename[:-3]}'
        try:
            importlib.import_module(module_name)
            bot.load_extension(module_name)
            print(f"Загружено расширение: {module_name}")
        except Exception as e:
            print(f"Не удалось загрузить {module_name}: {e}")

def main():
    to = "test"
    for i in range(len(sys.argv)):
        if sys.argv[i] == "-p":
            to = sys.argv[i+1]
    bot.run(json.loads(os.getenv('PROFILES'))[to])
