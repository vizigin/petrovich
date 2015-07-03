# -*- coding: utf-8 -*-
import time
import urlparse
import requests
from db import get_chats, activate, deactivate
from config import config

telegram_bot_url = str(config.get("telegram_bot_url"))
telegram_token = str(config.get("telegram_token"))
heroku_url = str(config.get("heroku_url"))

class Command:
	def __init__(self, bot, name):
		self.name = name

class ActivateCommand(Command):
	def __init__(self, bot, name):
		Command.__init__(self, bot, name)
		self.bot = bot

	def run(self, id):
		activate(id)
		self.bot.send_message(id, str(config.get("activate_message")))

class DeactivateCommand(Command):
	def __init__(self, bot, name):
		Command.__init__(self, bot, name)
		self.bot = bot

	def run(self, id):
		deactivate(id)
		self.bot.send_message(id, str(config.get("deactivate_message")))

class Bot:
	def __init__(self): 
		self.commands = []
		self.commands.append( ActivateCommand(self, str(config.get("activate_command"))) )
		self.commands.append( DeactivateCommand(self, str(config.get("deactivate_command"))) )

	def init_webhook(self):
		requests.get( telegram_bot_url + telegram_token + "/setWebhook", params={'url': heroku_url} )

	def execute(self, command_name, chat_id):
		print command_name
		for command in self.commands:
			print command.name
			if command.name == command_name:
				command.run(chat_id)
				return;

	def send_message(self, chat_id, text):
		params = {'chat_id': chat_id, 'text': text}
		requests.get( telegram_bot_url + telegram_token + "/sendMessage", params=params )

	def send_posts(self, posts):
		for post in posts:
			if insert_post(post) == True:
				send_message_all(post["text"])
				time.sleep(5)

	def send_message_all(self, text):
		chats = get_chats()
		for chat in chats:
			send_message(chat, text)
