from flask import Flask, request
from telegram import Update, InlineQueryResultPhoto
from telegram.ext import Application, InlineQueryHandler, ContextTypes
from duckduckgo_search import DDGS
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = f"https://{os.getenv('REPL_SLUG')}.{os.getenv('REPL_OWNER')}.repl.co"

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set")

# Telegram Bot setup
app = Flask(__name__)
telegram_app = Application.builder().token(BOT_TOKEN).build()

async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return

    with DDGS() as ddgs:
        results = ddgs.images(query, max_results=10)

    photos = []
    for i, r in enumerate(results):
        if 'image' in r:
            photos.append(
                InlineQueryResultPhoto(
                    id=str(i),
                    photo_url=r['image'],
                    thumbnail_url=r.get('thumbnail', r['image']),
                )
            )

    await update.inline_query.answer(photos)

telegram_app.add_handler(InlineQueryHandler(inline_query))

@app.route("/")
def home():
    return "Bot is alive!"

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    telegram_app.update_queue.put_nowait(update)
    return "ok"

if __name__ == "__main__":
    print("Starting webhook...")
    telegram_app.run_webhook(
        listen="0.0.0.0",
        port=8080,
        webhook_url=f"{WEBHOOK_URL}/{BOT_TOKEN}"
    )
