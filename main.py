import os
import requests
from telegram.ext import Updater, MessageHandler, Filters

TOKEN = os.getenv('BOT_TOKEN')
API_KEY = os.getenv('API_KEY')
IDS = os.getenv('IDS')
API_URL = os.getenv('API_URL')

def trigger_api(message):
    headers = {
        'x-api-key': API_KEY,
        'ids': IDS,
        'Content-Type': 'text/plain'
    }
    response = requests.post(API_URL, headers=headers, data=message)

    if response.status_code == 200:
        return response.text
    return f"Error: {response.status_code}"

def handle_message(update, context):
    user_message = update.message.text
    api_response = trigger_api(user_message)
    update.message.reply_text(f"Pesan kamu telah diteruskan. API Response: {api_response}")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
