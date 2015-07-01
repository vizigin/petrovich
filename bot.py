import urlparse
import requests
from config import config
from db import get_chats

telegram_bot_url = str(config.get("telegram_bot_url"))
telegram_token = str(config.get("telegram_token"))
heroku_url = str(config.get("heroku_url"))

def init_webhook():
	requests.get( telegram_bot_url + telegram_token + "/setWebhook", params={'url': heroku_url} )

def send_message(chat_id, text):
	params = {'chat_id': chat_id, 'text': text}
	requests.get( telegram_bot_url + telegram_token + "/sendMessage", params=params )

def send_message_all(text):
	chats = get_chats()
	for chat in chats:
		send_message(chat, text)

#init_webhook()