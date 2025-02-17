from disnake.ext import commands
import importlib.util
import disnake 
import os
import sys
import json
import settings
TOKEN = None
if not hasattr(os, "work_dir"):
    print("Set test floader.")
    os.work_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'test', 'work'))
    if not os.path.isdir(os.work_dir):
        os.makedirs(os.work_dir, exist_ok=True)
    TOKEN = "TOKEN"
    
from util.db import Data
import util.Resouces as res
meta = res.loadJsonObject("base")


bot = commands.Bot(
    command_prefix=meta.command_prefix,
    intents=disnake.Intents.all(),
    status=disnake.Status.online,
    activity=disnake.Activity(
        type=disnake.ActivityType.watching,
        name="Абема",
        url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")

)

cur = Data.getCur()

@bot.event
async def on_ready():
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
        except Exception as e:
            print(f"Не удалось загрузить {module_name}: {e}")

if __name__ == "__main__":
    to = "test"
    for i in range(len(sys.argv)):
        if sys.argv[i] == "-p":
            to = sys.argv[i+1]
    if TOKEN == None:
        TOKEN = f"{os.env_provider:Profiles:{to}}"
    bot.run(TOKEN)
