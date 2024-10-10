import os
import requests
import logging
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

# Konfigurasi logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Mengambil variabel dari environment
TOKEN = os.getenv('BOT_TOKEN')
API_KEY = os.getenv('API_KEY')
IDS = os.getenv('IDS')
API_URL = os.getenv('API_URL')  # URL API

def trigger_api(message):
    """Memicu API dengan pesan yang diterima."""
    headers = {
        'x-api-key': API_KEY,
        'ids': IDS,
        'Content-Type': 'text/plain'
    }
    response = requests.post(API_URL, headers=headers, data=message)

    if response.status_code == 200:
        return response.text
    return f"Error: {response.status_code}"

def handle_message(update: Update, context: CallbackContext):
    """Menangani pesan yang masuk dan meneruskannya ke API."""
    user_message = update.message.text
    logger.info(f"Pesan diterima: {user_message}")  # Tambahkan logging
    api_response = trigger_api(user_message)
    update.message.reply_text(f"Pesan kamu telah diteruskan. API Response: {api_response}")

def main():
    """Fungsi utama untuk menjalankan bot."""
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Menangani semua pesan teks
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Mengatur webhook
    PORT = int(os.environ.get('PORT', 5000))
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN)
    updater.bot.setWebhook(f'https://bot-telegram-samunu-6b58d8079dd0.herokuapp.com/{TOKEN}')

    # Menjalankan bot
    updater.idle()

if __name__ == '__main__':
    main()
