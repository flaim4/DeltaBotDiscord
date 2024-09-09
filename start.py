import os
import sys
import subprocess
import time

# Запускаем бота в отдельном процессе
def start_bot():
    return subprocess.Popen([sys.executable, "main.py"])

def main():
    bot_process = start_bot()

    while True:
        command = input("Введите команду (reload для перезагрузки): \n").strip().lower()

        if command == "reload":
            print("Перезагрузка бота...")
            bot_process.terminate()
            bot_process.wait()
            bot_process = start_bot()
            print("Бот перезапущен.")
        
        elif command == "exit":
            print("Завершение работы.")
            bot_process.terminate()
            bot_process.wait()
            break
        
        else:
            print("Неизвестная команда. Используйте 'reload' или 'exit'.")

if __name__ == "__main__":
    main()
