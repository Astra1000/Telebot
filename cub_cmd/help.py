from pyrogram.types import Message

async def help_command(client, message: Message):
    help_text = "🆘 **Список доступных команд**\n\n"
    help_text += "▸ `.ping` - Проверить работоспособность бота\n"
    help_text += "▸ `.version` - Показать версию и проверить обновления\n"
    help_text += "▸ `.update` - Обновить бота до последней версии\n"
    help_text += "▸ `.help` - Показать эту справку\n\n"
    help_text += "🔧 **Система кома��д**\n"
    help_text += "- Префиксы команд: `.`, `!`, `/`\n"
    help_text += "- Команды загружаются из папки `cub_cmd`\n"
    help_text += f"▸ Загружено команд: {len(client.command_handlers)}\n\n"
    help_text += f"🔖 Версия: {client.current_version}"
    
    await message.reply(help_text, disable_web_page_preview=True)

def register(handlers):
    handlers["help"] = help_command
    handlers["помощь"] = help_command
    handlers["start"] = help_command
