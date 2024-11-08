import os
import inspect
import disnake
import importlib

from utility.main import *
from utility.logs_tools import *
from disnake.ext import commands

def load_cogs(bot: commands.Bot, log: Log_Tools) -> None:
    for filename in os.listdir(os.path.dirname(__file__)):
        if (filename.endswith(".py") and filename != "__init__.py"):
            cog_name: str = filename[:-3]
            module: importlib.import_module = importlib.import_module(f"cogs.{cog_name}")

            for name, obj in inspect.getmembers(module, inspect.isclass):
                name: str
                obj: type
                if issubclass(obj, commands.Cog) and obj.__module__ == module.__name__:
                    bot.add_cog(obj(bot))
                    print_log(f"The class {name} is started.")
                    log.write_log(f"The class {name} is started.")
    