
import os
import importlib.util
from pyrogram import Client, filters
from pyrogram.types import Message
from configparser import ConfigParser
import sys

# Конфигурация
CONFIG_FILE = "config.ini"
COMMANDS_DIR = "cub_cmd"
PREFIXES = [".", "!", "/"]
REPO_URL = "https://github.com/astra1000/Telebot"  # ЗАМЕНИТЕ НА ВАШ РЕПОЗИТОРИЙ
VERSION_FILE = "version.txt"

def load_config() -> tuple:
    config = ConfigParser()
    if not os.path.exists(CONFIG_FILE):
        config["pyrogram"] = {
            "api_id": input("Введите API ID: "),
            "api_hash": input("Введите API HASH: ")
        }
        with open(CONFIG_FILE, "w") as f:
            config.write(f)
        print(f"Конфигурация сохранена в {CONFIG_FILE}")
    
    config.read(CONFIG_FILE)
    return (config["pyrogram"]["api_id"], config["pyrogram"]["api_hash"])

def load_commands():
    command_handlers = {}
    if not os.path.exists(COMMANDS_DIR):
        os.makedirs(COMMANDS_DIR)
        print(f"Создана папка команд: {COMMANDS_DIR}")
    
    for file in os.listdir(COMMANDS_DIR):
        if file.endswith(".py") and not file.startswith("_"):
            module_name = f"{COMMANDS_DIR}.{file[:-3]}"
            file_path = os.path.join(COMMANDS_DIR, file)
            
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            if hasattr(module, "register"):
                module.register(command_handlers)
                print(f"Загружена команда: {file}")
    
    return command_handlers

def get_current_version():
    if not os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, "w") as f:
            f.write("1.0.0")
        return "1.0.0"
    
    with open(VERSION_FILE, "r") as f:
        return f.read().strip()

# Создаем файл версии при отсутствии
if not os.path.exists(VERSION_FILE):
    with open(VERSION_FILE, "w") as f:
        f.write("1.0.0")

api_id, api_hash = load_config()
command_handlers = load_commands()
current_version = get_current_version()

app = Client("cub_bot", api_id=int(api_id), api_hash=api_hash)

# Диспетчер команд
@app.on_message(filters.private & filters.text)
async def command_dispatcher(client: Client, message: Message):
    if not message.text or message.text[0] not in PREFIXES:
        return
    
    command = message.text.split()[0][1:].lower()
    handler = command_handlers.get(command)
    
    if handler:
        await handler(client, message)

if __name__ == "__main__":
    print(f"🤖 Бот запущен | Версия: {current_version}")
    print(f"📂 Загружено команд: {len(command_handlers)}")
    print(f"🔑 Префиксы команд: {', '.join(PREFIXES)}")
    app.run()
