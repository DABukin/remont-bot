import os
import requests
from flask import Flask, request
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

TOKEN = os.environ.get("BOT_TOKEN")
FORM_URL = os.environ.get("FORM_URL")

OBJECT, AMOUNT, CATEGORY = range(3)

app_flask = Flask(__name__)

telegram_app = Application.builder().token(TOKEN).build()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет 👋\nНапиши /expense чтобы добавить расход."
    )


async def expense_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Введите ID объекта:")
    return OBJECT


async def get_object(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["object_id"] = update.message.text
    await update.message.reply_text("Введите сумму:")
    return AMOUNT


async def get_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["amount"] = update.message.text

    keyboard = [["материалы"], ["доставка"], ["инструмент"], ["расходники"], ["прочее"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

    await update.message.reply_text("Выберите категорию:", reply_markup=reply_markup)
    return CATEGORY


async def get_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    category = update.message.text
    object_id = context.user_data["object_id"]
    amount = context.user_data["amount"]

    data = {
        "entry.756291279": "AUTO",
        "entry.1422320460": object_id,
        "entry.656508705": "2026-02-15",
        "entry.577364935": amount,
        "entry.379656384": category
    }

    response = requests.post(FORM_URL, data=data)

    if response.status_code in (200, 302):
        await update.message.reply_text("✅ Расход добавлен!")
    else:
        await update.message.reply_text("❌ Ошибка при отправке.")

    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[CommandHandler("expense", expense_start)],
    states={
        OBJECT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_object)],
        AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_amount)],
        CATEGORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_category)],
    },
    fallbacks=[],
)

telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(conv_handler)


@app_flask.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    telegram_app.process_update(update)
    return "ok"


@app_flask.route("/")
def home():
    return "Bot is running"


if __name__ == "__main__":
    app_flask.run(host="0.0.0.0", port=10000)
