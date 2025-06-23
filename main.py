from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from openai import OpenAI
import os

TELEGRAM_BOT_TOKEN = os.getenv("7606752566:AAEh11nA21O9Eoj8tt44eeHduyRR5TXFSpM")
OPENAI_API_KEY = os.getenv("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")

client = OpenAI(api_key=OPENAI_API_KEY)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.voice:
        voice_file = await update.message.voice.get_file()
        voice_path = await voice_file.download_to_drive()
        audio_data = open(voice_path.name, "rb")
        transcription = client.audio.transcriptions.create(model="whisper-1", file=audio_data)
        user_input = transcription.text
    else:
        user_input = update.message.text

    chat_completion = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": user_input}]
    )
    bot_reply = chat_completion.choices[0].message.content
    await update.message.reply_text(bot_reply)

app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT | filters.VOICE, handle_message))
app.run_polling()
