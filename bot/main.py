import os
import subprocess
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "🤖 **Бот-Аудитор Безопасности запущен!**\n\n"
        "Используй команды для проверки изоляции контейнера:\n"
        "1. /whoami — узнать текущего пользователя внутри контейнера\n"
        "2. /test_write — попробовать создать файл (проверка Read-Only)\n"
        "3. /check_socket — проверить доступ к сокету Docker\n"
        "4. /cmd <команда> — выполнить произвольную консольную команду"
    )
    await update.message.reply_markdown(msg)

# Команда 1: Кто я?
async def whoami(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = subprocess.getoutput("whoami")
    uid = subprocess.getoutput("id -u")
    await update.message.reply_text(f"👤 Текущий пользователь: {user} (UID: {uid})")

# Команда 2: Попытка записи
async def test_write(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        with open("/app/test_hack.txt", "w") as f:
            f.write("Hacked!")
        await update.message.reply_text("⚠️ ОПАСНОСТЬ: Файл успешно создан! Защита Read-Only НЕ работает.")
    except Exception as e:
        await update.message.reply_text(f"🛡️ ЗАЩИТА СРАБОТАЛА!\nОшибка при записи: {e}")

# Команда 3: Проверка Docker Socket
async def check_socket(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if os.path.exists("/var/run/docker.sock"):
        await update.message.reply_text("⚠️ УЯЗВИМОСТЬ: Docker Socket найден! Возможен Container Escape.")
    else:
        await update.message.reply_text("🛡️ БЕЗОПАСНО: Docker Socket отсутствует в контейнере.")

# Команда 4: Выполнение произвольной команды
async def run_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    command = " ".join(context.args)
    if not command:
        await update.message.reply_text("Укажите команду, например: /cmd ls -la /")
        return
    output = subprocess.getoutput(command)
    await update.message.reply_text(f"🖥️ Результат выполнения `{command}`:\n```\n{output}\n```", parse_mode="Markdown")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("whoami", whoami))
    app.add_handler(CommandHandler("test_write", test_write))
    app.add_handler(CommandHandler("check_socket", check_socket))
    app.add_handler(CommandHandler("cmd", run_cmd))
    app.run_polling()