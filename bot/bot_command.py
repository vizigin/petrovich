#-*- coding: utf-8 -*-
from chat import *
import time
import botan

class BotCommand:
	def __init__(self, bot, name):
		self.name = name

class HelpCommand(BotCommand):
	def __init__(self, bot, name):
		BotCommand.__init__(self, bot, name)
		self.bot = bot
	def run(self, id, args, message_date):
		self.bot.broadcast_message(id, str(config.get("hello_message")))
		botan.track(str(config.get("ya_token")), id, {}, 'HelpCommand')

class RandomCommand(BotCommand):
	def __init__(self, bot, name):
		BotCommand.__init__(self, bot, name)
		self.bot = bot
	def run(self, id, args, message_date):
		self.bot.broadcast_message(id, str(get_random_post()))
		botan.track(str(config.get("ya_token")), id, {}, 'RandomCommand')

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
			botan.track(str(config.get("ya_token")), id, {}, 'SearchCommand')

class LastCommand(BotCommand):
	def __init__(self, bot, name):
		BotCommand.__init__(self, bot, name)
		self.bot = bot
	def run(self, id, args, message_date):
		channels = config.get("channels");
		if len(channels) == 1:
			self.send_last_posts(id, channels[0]["name"])
			botan.track(str(config.get("ya_token")), id, {}, 'LastCommand')
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
			botan.track(str(config.get("ya_token")), id, {}, 'LastCommand')
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
	def check_status(self, id, args):
		c = Chat(id)
		channels = config.get("channels");
		min_args = 1 if (len(channels) > 1) else 0
		if (len(args) < min_args):
			status = "Текущие подписки:\n" + c.get_full_status()
			self.bot.broadcast_message(id, str(config.get("subscribe_message")) + "\n\n" + status)
			return True;
		return False;
	def subscribe(self, id, channel, subscription_type, message):
		c = Chat(id)
		try:
			print channel, subscription_type
			c.subscribe(channel, subscription_type)
			self.bot.broadcast_message(id, message)
		except NameError:
			self.bot.broadcast_message(id, str(config.get("doesntexist_message")))


class SubscribeStopCommand(SubscribeCommand):
	def __init__(self, bot, name):
		BotCommand.__init__(self, bot, name)
		self.bot = bot
	def run(self, id, args, message_date):
		if self.check_status(id, args) == False:
			c = Chat(id)
			botan.track(str(config.get("ya_token")), id, {}, 'SubscribeStopCommand')
			channels = config.get("channels");
			channel = args[0] if (len(channels) > 1) else channels[0]["name"]
			try:
				c.unsubscribe_all(channel)
				message = str(config.get("stop_message"))
				self.bot.broadcast_message(id, message)
			except NameError:
				self.bot.broadcast_message(id, str(config.get("doesntexist_message")))

class SubscribeDailyCommand(SubscribeCommand):
	def __init__(self, bot, name):
		SubscribeCommand.__init__(self, bot, name)
	def run(self, id, args, message_date):
		if self.check_status(id, args) == False:
			botan.track(str(config.get("ya_token")), id, {}, 'SubscribeDailyCommand')
			channels = config.get("channels");
			channel = args[0] if (len(channels) > 1) else channels[0]["name"]
			self.subscribe(id, channel, Type.Daily, str(config.get("daily_message")))

class SubscribeHourlyCommand(SubscribeCommand):
	def __init__(self, bot, name):
		SubscribeCommand.__init__(self, bot, name)
	def run(self, id, args, message_date):
		if self.check_status(id, args) == False:
			botan.track(str(config.get("ya_token")), id, {}, 'SubscribeHourlyCommand')
			channels = config.get("channels");
			channel = args[0] if (len(channels) > 1) else channels[0]["name"]
			self.subscribe(id, channel, Type.Hourly, str(config.get("hourly_message")))

class SubscribeAutoCommand(SubscribeCommand):
	def __init__(self, bot, name):
		SubscribeCommand.__init__(self, bot, name)
	def run(self, id, args, message_date):
		if self.check_status(id, args) == False:
			botan.track(str(config.get("ya_token")), id, {}, 'SubscribeAutoCommand')
			channels = config.get("channels");
			channel = args[0] if (len(channels) > 1) else channels[0]["name"]
			self.subscribe(id, channel, Type.Auto, str(config.get("auto_message")))
