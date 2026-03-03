import json
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ------------------------
# KONFIGURACJA
# ------------------------
TOKEN = os.environ.get("TOKEN")         # Token bota z BotFather
OWNER_ID = int(os.environ.get("OWNER_ID"))  # Twój Telegram ID
DEFAULT_MESSAGE = "😈😈😈"              # Domyślna wiadomość

GROUPS_FILE = "groups.json"
MESSAGE_FILE = "message.json"

# ------------------------
# Funkcje pomocnicze
# ------------------------
def load_groups():
    if os.path.exists(GROUPS_FILE):
        with open(GROUPS_FILE, "r") as f:
            return json.load(f)
    return []

def save_groups(groups):
    with open(GROUPS_FILE, "w") as f:
        json.dump(groups, f)

def load_message():
    if os.path.exists(MESSAGE_FILE):
        with open(MESSAGE_FILE, "r") as f:
            return json.load(f).get("message", DEFAULT_MESSAGE)
    return DEFAULT_MESSAGE

def save_message(msg):
    with open(MESSAGE_FILE, "w") as f:
        json.dump({"message": msg}, f)

# ------------------------
# Komendy bota
# ------------------------
async def dodaj(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return
    chat_id = update.effective_chat.id
    groups = load_groups()
    if chat_id not in groups:
        groups.append(chat_id)
        save_groups(groups)
        await update.message.reply_text("Grupa dodana 😈")
    else:
        await update.message.reply_text("Ta grupa już jest zapisana.")

async def usun(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return
    chat_id = update.effective_chat.id
    groups = load_groups()
    if chat_id in groups:
        groups.remove(chat_id)
        save_groups(groups)
        await update.message.reply_text("Grupa usunięta.")
    else:
        await update.message.reply_text("Ta grupa nie jest zapisana.")

async def lista(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return
    groups = load_groups()
    if groups:
        await update.message.reply_text(f"Zapisane grupy:\n{groups}")
    else:
        await update.message.reply_text("Brak zapisanych grup.")

async def diabel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return
    msg = load_message()
    groups = load_groups()
    for group_id in groups:
        try:
            await context.bot.send_message(chat_id=group_id, text=msg)
        except:
            pass
    await update.message.reply_text("Wysłano wiadomość do wszystkich grup 😈")

async def ustaw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return
    if not context.args:
        await update.message.reply_text("Użyj: /ustaw <wiadomość>")
        return
    new_msg = " ".join(context.args)
    save_message(new_msg)
    await update.message.reply_text(f"Wiadomość ustawiona na:\n{new_msg}")

# ------------------------
# Start bota
# ------------------------
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("dodaj", dodaj))
app.add_handler(CommandHandler("usun", usun))
app.add_handler(CommandHandler("lista", lista))
app.add_handler(CommandHandler("diabel", diabel))
app.add_handler(CommandHandler("ustaw", ustaw))

print("Bot działa...")
app.run_polling()
