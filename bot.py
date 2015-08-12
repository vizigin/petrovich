# -*- coding: utf-8 -*-
import time
import re
import urlparse
import requests
import json
from db import get_chats, insert_post
from config import config
from bot_command import *

telegram_bot_url = str(config.get("telegram_bot_url"))
telegram_token = str(config.get("telegram_token"))
heroku_url = str(config.get("heroku_url"))

class Bot:
	def __init__(self): 
		self.commands = []
		self.commands.append( LastCommand(self, str(config.get("commands")[0])) )
		self.commands.append( FlowCommand(self, str(config.get("commands")[2])) )
		self.commands.append( SettingsCommand(self, str(config.get("commands")[3])) )
		self.commands.append( HelpCommand(self, str(config.get("commands")[4])) )

	def execute(self, command_name, chat_id, arg):
		for command in self.commands:
			if command.name == command_name:
				command.run(chat_id, arg)
				return;

	def decode_command(self, text):
		commands = config.get("commands")
		regex = re.compile(r"([/?]\w+)\b")
		parsed_command = re.findall(regex, text)
		for command in commands:
			if command == parsed_command[0]:
				return command
		raise KeyError('Command not found')

	def init_webhook(self):
		requests.get( telegram_bot_url + telegram_token + "/setWebhook", params={'url': heroku_url} )
		
	def send_message(self, chat_id, text, keys=[]):
		params = {'chat_id': chat_id, 'text': text, 'reply_markup': json.dumps({"keyboard":keys, 'one_time_keyboard':True})}
		r = requests.get( telegram_bot_url + telegram_token + "/sendMessage", params=params )
		return r.json()["ok"]

	def send_message_all(self, text):
		chats = get_chats()
		for chat in chats:
			self.send_message(chat, text)

	def send_posts(self, posts):
		for post in posts:
			if insert_post(post) == True:
				self.send_message_all(post["text"])
				time.sleep(5)