import os
import subprocess
import requests
from pyrogram.types import Message

async def update_command(client, message: Message):
    try:
        # Получаем ссылку на последнюю версию
        api_url = REPO_URL.replace("github.com", "api.github.com/repos") + "/releases/latest"
        response = requests.get(api_url)
        if response.status_code != 200:
            await message.reply("❌ Не удалось получить информацию о последней версии")
            return
            
        release_data = response.json()
        latest_version = release_data["tag_name"]
        if latest_version.startswith('v'):
            latest_version = latest_version[1:]
        
        # Проверяем нужно ли обновление
        if latest_version == client.current_version:
            await message.reply(f"✅ У вас уже установлена последняя версия `{client.current_version}`")
            return
        
        # Обновляем через git
        if os.path.exists(".git"):
            # Выполняем git pull
            result = subprocess.run(["git", "pull"], capture_output=True, text=True)
            if result.returncode != 0:
                await message.reply(f"❌ Ошибка при обновлении:\n```\n{result.stderr}\n```")
                return
                
            # Обновляем файл версии
            with open(VERSION_FILE, "w") as f:
                f.write(latest_version)
                
            await message.reply(
                f"✅ Обновление успешно завершено!\n"
                f"▸ Новая версия: `{latest_version}`\n\n"
                "Перезапустите бота командой:\n"
                "`python main.py`"
            )
        else:
            # Для пользователей без git - даем ссылку
            zip_url = f"{REPO_URL}/archive/refs/tags/v{latest_version}.zip"
            await message.reply(
                f"⚠️ Для обновления скачайте новую версию:\n{zip_url}\n\n"
                "Или клонируйте репозиторий заново:\n"
                f"`git clone {REPO_URL}`\n\n"
                "После обновления не забудьте:\n"
                "1. Скопировать ваш `config.ini`\n"
                "2. Установить зависимости: `pip install -r requirements.txt`"
            )
            
    except Exception as e:
        await message.reply(f"❌ Ошибка при обновлении: {str(e)}")

def register(handlers):
    handlers["update"] = update_command
    handlers["upd"] = update_command
    handlers["обновить"] = update_command
