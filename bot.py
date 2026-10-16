import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Aapke credentials
BOT_TOKEN = "7747802874:AAHOutm2e7qXqS5x9_m1Ksn4jZ8XG31bU8M"
FISH_API_KEY = "sk-f1sh-30dc2f45df46-ac2d-fc6eeb6_ZCBXKvXG5F0RP2Z18UY"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Namaste! Mujhe koi bhi text bhejo, main usko audio bana kar bhejunga.")

async def text_to_speech(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    status_msg = await update.message.reply_text("Audio generate ho raha hai, thoda intezaar karein...")

    url = "https://api.fish.audio/v1/tts"
    headers = {
        "Authorization": f"Bearer {FISH_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "format": "mp3"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            audio_path = "output.mp3"
            with open(audio_path, "wb") as f:
                f.write(response.content)

            with open(audio_path, "rb") as audio:
                await update.message.reply_voice(voice=audio)

            os.remove(audio_path)
            await status_msg.delete()
        else:
            await status_msg.edit_text(f"Error aaya: {response.status_code}")
    except Exception as e:
        await status_msg.edit_text(f"Kuch gadbad hui: {e}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_to_speech))

    print("Bot chal raha hai...")
    app.run_polling()
