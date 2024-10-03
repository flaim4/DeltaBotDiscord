import os
import json

from datetime import datetime

def print_log(text: str) -> None: 
    current_time: datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{current_time}] {text}")

def load_json() -> json.load: 
    json_path: os.path.join = os.path.join("./config", "welcome.json")
    with open(json_path, "r", encoding="utf-8") as file:
        return json.load(file)["messages"]
