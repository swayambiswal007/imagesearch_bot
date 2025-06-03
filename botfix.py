from telegram import InlineQueryResultPhoto, Update
from telegram.ext import ApplicationBuilder, InlineQueryHandler, ContextTypes
from duckduckgo_search import DDGS  # Correct class name
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")


async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return
    
    with DDGS() as ddgs:
        results = ddgs.images(query, max_results=25)  # this returns a generator
    
    photos = []
    for i, r in enumerate(results):
        if 'image' in r:
            photos.append(
                InlineQueryResultPhoto(
                    id=str(i),
                    photo_url=r['image'],
                    thumb_url=r.get('thumbnail', r['image']),
                )
            )
    
    await update.inline_query.answer(photos)
print("BOT_TOKEN:", BOT_TOKEN)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(InlineQueryHandler(inline_query))
    print("Bot is running...")
    app.run_polling()
