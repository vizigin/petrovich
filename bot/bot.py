# -*- coding: utf-8 -*-
from db import get_subscripted_chats, create, clear
from config import config
from bot_command import *
import urlparse
import requests
import time
import json
import re
import datetime
from datetime import date, timedelta

telegram_bot_url = str(config.get("telegram_bot_url"))
telegram_token = str(config.get("telegram_token"))
heroku_url = str(config.get("heroku_url"))

class Bot:
	def __init__(self): 
		self.commands = []
		self.commands.append( LastCommand(self, str(config.get("commands")[0])) )
		self.commands.append( SearchCommand(self, str(config.get("commands")[1])) )
		self.commands.append( RandomCommand(self, str(config.get("commands")[2])) )
		self.commands.append( SubscribeCommand(self, str(config.get("commands")[3])) )
		self.commands.append( HelpCommand(self, str(config.get("commands")[4])) )

	def configure(self):
		#r = requests.get( telegram_bot_url + telegram_token + "/setWebhook", params={'url': heroku_url} )
		#сreate()
		current_date = time.time()
		insert_digest_date(current_date)

	def clear(self):
		r = requests.get( telegram_bot_url + telegram_token + "/setWebhook", params={'url': ""} )
		print r
		clear()

	def execute(self, command_name, chat_id, args, date):
		for command in self.commands:
			if command.name == command_name:
				command.run(chat_id, args, date)
				return;

	def decode_command(self, text):
		commands = config.get("commands")
		regex = re.compile(r"([/?]\w+)\b")
		parsed_command = re.findall(regex, text)
		if len(parsed_command) == 0:
			raise KeyError('Command not found')
		for command in commands:
			if command == parsed_command[0]:
				return command
		raise KeyError('Command not found')
		
	def broadcast_message(self, chat_id, text, keys=[]):
		text = text[0:2000] if len(text) > 2000 else text
		params = {'chat_id': chat_id, 'text': text, 'reply_markup': json.dumps({"keyboard":keys, 'one_time_keyboard':True})}
		r = requests.get( telegram_bot_url + telegram_token + "/sendMessage", params=params )
		print r
		return r.json()["ok"]			

	def broadcast_post(self, post, channel):
		chats = get_subscripted_chats(channel)
		for chat in chats:
			self.broadcast_message(chat, post["text"])
			time.sleep(5)