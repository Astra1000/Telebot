import time

async def ping_command(client, message):
    start = time.time()
    ping_msg = await message.reply("🏓 PONG !")
    latency = round((time.time() - start) * 1000, 2)
    await ping_msg.edit_text(
        f"🏓 PONG !\n"
        "✅ Бот успешно функционирует.\n"
        f"⏱️ Ответил за: {latency} мс\n"
        f"🔖 Версия: {client.current_version}"
    )

def register(handlers):
    handlers["ping"] = ping_command
    handlers["пинг"] = ping_command
    handlers["test"] = ping_command
    handlers["тест"] = ping_command
