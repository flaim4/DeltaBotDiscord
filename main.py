from disnake.ext import commands
import importlib.util
import disnake 
import os
import sys
import logging

formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    "%H:%M:%S"
)

a = logging.FileHandler("app.log")
a.setFormatter(formatter)
b = logging.StreamHandler()
b.setFormatter(formatter)

logging.basicConfig(
    level=logging.INFO,
    handlers=[
        a, b
    ]
)

sys.path.insert(0, os.path.abspath('.'))
os.work_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'work'))
if not os.path.isdir(os.work_dir):
    os.makedirs(os.work_dir, exist_ok=True)

from util.service import ServiceRegistry
from util.config import ConfigService
from util.db import Data
import util.Resouces as res
from multienv import EnvMannager, IniEnvProvider

env : EnvMannager = EnvMannager()
env += IniEnvProvider("env.ini")
env.load()
env.setGlobal()

config = res.from_dict(ConfigService, res.loadYaml("base"))
ServiceRegistry.register("config", config)

bot = commands.Bot(
    command_prefix=config.command_prefix,
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
    logging.info('Successful login in: ' + str(bot.user))


for filename in os.listdir('./cogs'):
    if filename.endswith('.py') and filename != "_init_.py":
        file_path = os.path.join('./cogs', filename)

        spec = importlib.util.spec_from_file_location(filename[:-3], file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        class_dict = {name: obj for name, obj in vars(module).items() if isinstance(obj, type)}
        if filename[:-3] in class_dict:
            cls = class_dict[filename[:-3]]
            cls.logger = logging.getLogger(filename[:-3])
            if cls.id in config.cogs and config.cogs[cls.id].enable:
                obj = cls(bot)
                ServiceRegistry.register(cls.id, obj)

if __name__ == "__main__":
    to = "test"
    for i in range(len(sys.argv)):
        if sys.argv[i] == "-p":
            to = sys.argv[i+1]
    bot.run(f"{os.env_provider:profiles:{to}}")
