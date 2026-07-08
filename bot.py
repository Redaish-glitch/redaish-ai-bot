import os
from groq import Groq
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Saya AI Bot. Silakan kirim pertanyaan.")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Kamu adalah asisten AI yang ramah."},
            {"role": "user", "content": user_message}
        ]
    )

    reply = response.choices[0].message.content
    await update.message.reply_text(reply)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

app.run_polling()
