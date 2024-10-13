import datetime

from typing import TextIO
from datetime import datetime

class Log_Tools:

    def __init__(self):
        self.name: datetime = self.log_init()

    def log_init(self) -> datetime:
        current_time: datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        w: TextIO = open(f'logs/{current_time}.log', 'a')
        w.close()
        return current_time

    def write_log(self, text: str) -> None:
        current_time: datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        w: TextIO = open(f'logs/{self.name}.log', 'a', encoding = "UTF-8")
        w.write(f"[{current_time}] {text}\n")
        w.close()
