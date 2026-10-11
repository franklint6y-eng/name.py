import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, CopyTextButton, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# 🔑 Replace with your token from @BotFather
TOKEN = "8672747467:AAF4yK4E5WeQjIpqTcG86zSn3VHwrTkW2-M"


def get_random_english_name():
    """Fetch a random English name from randomuser.me (GB nationality)"""
    try:
        response = requests.get("https://randomuser.me/api/?nat=gb&results=1", timeout=5)
        data = response.json()
        name = data["results"][0]["name"]
        return f"{name['first'].title()} {name['last'].title()}"
    except Exception:
        return "Unknown Name"


MAIN_KB = ReplyKeyboardMarkup(
    [[KeyboardButton("🎲 Generate Name")]],
    resize_keyboard=True,
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 *Welcome to the English Name Generator Bot!*\n\n"
        "Press the button below or use /name to get a random English full name.\n"
        "Tap the copy button to copy it instantly!",
        parse_mode="Markdown",
        reply_markup=MAIN_KB,
    )


async def send_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    generated_name = get_random_english_name()
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(f"📋 Copy: {generated_name}", copy_text=CopyTextButton(text=generated_name))]
    ])
    await update.message.reply_text(
        f"✨ *Your random English name:*\n\n`{generated_name}`",
        parse_mode="Markdown",
        reply_markup=keyboard,
    )

async def name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_name(update, context)

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "🎲 Generate Name":
        await send_name(update, context)


async def copy_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer(f"✅ Copied: {query.data}", show_alert=True)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ *Commands:*\n\n"
        "/name — Generate a random English name\n"
        "/start — Welcome message\n"
        "/help  — Show this message",
        parse_mode="Markdown"
    )


if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("name", name))
    app.add_handler(CallbackQueryHandler(copy_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_button))
    print("✅ Bot is running...")
    app.run_polling()
