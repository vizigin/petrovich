#-*- coding: utf-8 -*-
from chat import *

class BotCommand:
	def __init__(self, bot, name):
		self.name = name

class LastCommand(BotCommand):
	def __init__(self, bot, name):
		BotCommand.__init__(self, bot, name)
		self.bot = bot
	def run(self, id, arg):
		self.bot.send_message(id, "Здесь будут последние 5 новостей:")

class SettingsCommand(BotCommand):
	def __init__(self, bot, name):
		BotCommand.__init__(self, bot, name)
		self.bot = bot
	def run(self, id, arg):
		c = Chat(id)
		c.deconfigure()
		flow = "выключен" if c.get_mode_config()['flow'] == 'None' else "включен"
		digest = "выключен" if c.get_mode_config()['digest'] == 'None' else "включен. Следующий дайджест придёт " + c.get_digest_date().strftime('%d.%m.%Y в %H:%M')
		self.bot.send_message(id, "В данный момент бот настроен:\nПоток: " + flow + "\nДайджест: " + digest + "\n\nПри помощи клавиатуры вы можете обновить текущие настройки", [['Поток'],['Дайджест'],['Отмена']])

class HelpCommand(BotCommand):
	def __init__(self, bot, name):
		BotCommand.__init__(self, bot, name)
		self.bot = bot
	def run(self, id, arg):
		command1 = "/last - присылает последние пять новостей"
		command2 = "/flow on(off) - включает/выключает текущий поток новостей"
		command3 = "/digest on(off) - включает/выключает текущий дайджест"
		command4 = "/settings - здесь можно обновить настройки отправки новостей"
		command5 = "/help - список команд"
		self.bot.send_message(id, "Бот поддерживает следующие команды:\n" + command1 + "\n" + command2 + "\n" + command3 + "\n" + command4 + "\n" + command5)

class FlowCommand(BotCommand):
	def __init__(self, bot, name):
		BotCommand.__init__(self, bot, name)
		self.bot = bot
	def run(self, id, arg):
		c = Chat(id)
		status = ""
		if arg == "":
			status = "Поток выключен" if c.get_mode_config()['flow'] == 'None' else "Поток включен"
			status += "\non/off - включает/выключает поток"

		if arg == "on":
			if c.get_mode_config()['flow'] == 'None':
				c.set_flow_mode('Flow')
				status = "Поток включен"
			else:
				status = "Поток уже включен"

		if arg == "off":
			if c.get_mode_config()['flow'] == 'Flow':
				c.set_flow_mode('None')
				status = "Поток выключен"
			else:
				status = "Поток уже выключен"

		self.bot.send_message(id, status)
