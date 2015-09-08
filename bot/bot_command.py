#-*- coding: utf-8 -*-
from chat import *
import time

class BotCommand:
	def __init__(self, bot, name):
		self.name = name

class HelpCommand(BotCommand):
	def __init__(self, bot, name):
		BotCommand.__init__(self, bot, name)
		self.bot = bot
	def run(self, id, args, message_date):
		self.bot.broadcast_message(id, str(config.get("help_message")))

class RandomCommand(BotCommand):
	def __init__(self, bot, name):
		BotCommand.__init__(self, bot, name)
		self.bot = bot
	def run(self, id, args, message_date):
		self.bot.broadcast_message(id, str(get_random_post()))

class SearchCommand(BotCommand):
	def __init__(self, bot, name):
		BotCommand.__init__(self, bot, name)
		self.bot = bot
	def run(self, id, args, message_date):
		message = ""
		if (len(args) > 0):
			word = args[0]
			post_texts = search_posts(word)
			for post_text in post_texts:
				message += post_text[0] + "\n\n"
			message = "Постов не найдено" if message == "" else message
			self.bot.broadcast_message(id, message)

class LastCommand(BotCommand):
	def __init__(self, bot, name):
		BotCommand.__init__(self, bot, name)
		self.bot = bot
	def run(self, id, args, message_date):
		channels = config.get("channels");
		if len(channels) == 1:
			self.send_last_posts(id, channels[0]["name"])
			return;

		if (len(args) > 0):
			post_type = str(args[0])
			for c in channels:
				if c['name'] == post_type and c['forced'] == False:
					self.send_last_posts(id, post_type)
					return;
			self.bot.broadcast_message(id, str(config.get("doesntexist_message")))
		else:
			self.bot.broadcast_message(id, str(config.get("last_message")))
	def send_last_posts(self, id, channel):
		message = ""
		post_texts = get_last_posts(channel)
		for post_text in post_texts:
			message += post_text[0] + "\n\n"
		self.bot.broadcast_message(id, message)

class SubscribeCommand(BotCommand):
	def __init__(self, bot, name):
		BotCommand.__init__(self, bot, name)
		self.bot = bot
	def run(self, id, args, message_date):
		c = Chat(id)
		channels = config.get("channels");
		min_args = 1 if (len(channels) > 1) else 0

		# STATUS
		if (len(args) <= min_args):
			status = "Текущие подписки:\n" + c.get_full_status()
			self.bot.broadcast_message(id, str(config.get("subscribe_message")) + "\n\n" + status)
			return;

		channel = args[0] if (len(channels) > 1) else channels[0]["name"]
		command = args[1] if (len(channels) > 1) else args[0]
		
		print channel
		if command == Type.Stop:
			try:
				c.unsubscribe_all(channel)
				message = str(config.get("stop_message"))
				self.bot.broadcast_message(id, message)
			except NameError:
				self.bot.broadcast_message(id, str(config.get("doesntexist_message")))
			return

		if command == Type.Auto:
			try:
				c.subscribe(channel, Type.Auto)
				message = str(config.get("auto_message"))
				self.bot.broadcast_message(id, message)
			except NameError:
				self.bot.broadcast_message(id, str(config.get("doesntexist_message")))
			return

		if command == Type.Hourly:
			try:
				c.subscribe(channel, Type.Hourly)
				message = str(config.get("hourly_message"))
				self.bot.broadcast_message(id, message)
			except NameError:
				self.bot.broadcast_message(id, str(config.get("doesntexist_message")))
			return

		if command == Type.Daily:
			try:
				c.subscribe(channel, Type.Daily)
				message = str(config.get("daily_message"))
				self.bot.broadcast_message(id, message)
			except NameError:
				self.bot.broadcast_message(id, str(config.get("doesntexist_message")))
			return