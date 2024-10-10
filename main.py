import os
import requests
from telegram.ext import Updater, MessageHandler, Filters

# Mengambil variabel dari environment
TOKEN = os.getenv('BOT_TOKEN')
API_KEY = os.getenv('API_KEY')
IDS = os.getenv('IDS')

def trigger_api(message):
    """Memicu API dengan pesan yang diterima."""
    url = "https://bot.nestorzamili.works/send-plaintext"
    headers = {
        'x-api-key': API_KEY,
        'ids': IDS,
        'Content-Type': 'text/plain'
    }
    response = requests.post(url, headers=headers, data=message)

    if response.status_code == 200:
        return response.text
    return f"Error: {response.status_code}"

def handle_message(update, context):
    """Menangani pesan yang masuk dan meneruskannya ke API."""
    user_message = update.message.text
    api_response = trigger_api(user_message)
    update.message.reply_text(f"Pesan kamu telah diteruskan. API Response: {api_response}")

def main():
    """Fungsi utama untuk menjalankan bot."""
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Menangani semua pesan teks
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
