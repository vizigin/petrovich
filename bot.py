import urlparse
import requests
from config import config
from db import get_users

telegram_bot_url = str(config.get("telegram_bot_url"))
telegram_token = str(config.get("telegram_token"))
heroku_url = str(config.get("heroku_url"))

def init_webhook():
	requests.get( telegram_bot_url + telegram_token + "/setWebhook", params={'url': heroku_url} )

def send_message(userId, text):
	params = {'chat_id': userId, 'text': text}
	requests.get( telegram_bot_url + telegram_token + "/sendMessage", params=params )

def send_message_all(text):
	users = get_users()
	for user in users:
		send_message(user, text)

#init_webhook()