from telegram import InlineQueryResultPhoto, Update
from telegram.ext import ApplicationBuilder, InlineQueryHandler, ContextTypes
from duckduckgo_search import DDGS
import os

# For local development (.env support)
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("Error: BOT_TOKEN is not set. Please set it as an environment variable.")

async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return

    with DDGS() as ddgs:
        results = ddgs.images(query, max_results=25)

    photos = []
    for i, r in enumerate(results):
        if 'image' in r:
            photos.append(
                InlineQueryResultPhoto(
                    id=str(i),
                    photo_url=r['image'],
                    thumbnail_url=r.get('thumbnail', r['image']),  # ✅ FIXED HERE
                )
            )

    await update.inline_query.answer(photos)

if __name__ == "__main__":
    print("Starting bot...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(InlineQueryHandler(inline_query))
    print("Bot is running...")
    app.run_polling()
