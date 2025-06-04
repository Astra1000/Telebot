import requests
from pyrogram.types import Message

async def version_command(client, message: Message):
    # Получаем информацию о последнем релизе
    try:
        api_url = REPO_URL.replace("github.com", "api.github.com/repos") + "/releases/latest"
        response = requests.get(api_url)
        if response.status_code == 200:
            release_data = response.json()
            latest_version = release_data["tag_name"]
            if latest_version.startswith('v'):
                latest_version = latest_version[1:]
        else:
            latest_version = None
    except:
        latest_version = None

    # Формируем сообщение
    message_text = f"ℹ️ **Информация о версии**\n\n"
    message_text += f"▸ **Текущая версия:** `{client.current_version}`\n"
    
    if latest_version:
        if latest_version == client.current_version:
            message_text += f"▸ **Последняя версия:** `{latest_version}` (у вас актуальная версия)\n"
        else:
            message_text += f"▸ **Доступно обновление!**\n"
            message_text += f"▸ **Новая версия:** `{latest_version}`\n\n"
            message_text += f"Используйте команду `.update` для обновления"
    else:
        message_text += "▸ Не удалось проверить обновления\n"
    
    message_text += f"\n🔗 Репозиторий: {REPO_URL}"
    
    await message.reply(message_text, disable_web_page_preview=True)

def register(handlers):
    handlers["version"] = version_command
    handlers["ver"] = version_command
    handlers["v"] = version_command
