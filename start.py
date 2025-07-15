import os
import sys
import subprocess
from subprocess import Popen
import asyncio

def start_bot():
    return subprocess.Popen([sys.executable, "main.py"])

async def main():
    bot_process: Popen = start_bot()

    while True:
        command = input("Введите команду (reload для перезагрузки): \n").strip().lower()

        if command == "reload":
            print("Перезагрузка бота...")
            bot_process.terminate()
            bot_process.wait()
            bot_process = start_bot()
            print("Бот перезапущен.")
        
        elif command == "stop":
            print("Завершение работы.")
            bot_process.terminate()
            bot_process.wait()
            break
        
        else:
            print("Неизвестная команда. Используйте 'reload' или 'stop'.")

if __name__ == "__main__":
    asyncio.run(main())
