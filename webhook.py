#-*- coding: utf-8 -*-

# botan аналитика
# лендинг
# проблемы с клавиатурами
# обработка команд

import os
import logging
from config import config
from bottle import run, request, post
from bot import Bot
from chat import Chat, ConfigurationStatus

from db import configure_chat

bot = Bot()

@post("/")
def subscribe():
	try:
		message = unicode(request.json['message']['text'])
		chat_id = request.json['message']['chat']['id']
		date = request.json['message']['date']
		process(chat_id, message, date);
	except KeyError:
		print "Nothing to send"

def process(chat_id, message, date):
	chat = Chat(chat_id)
	if chat.is_exist() == False:
		chat.create()
		bot.send_message(chat_id, str(config.get("hello_message")), [['Поток'],['Дайджест']] );
	else:
		if chat.is_configure() == False:
			if message == "Отмена".decode('utf8'):
				configure_chat(chat_id)
				return;

			status = chat.configure(message, date)
			if status == ConfigurationStatus.DigestActivated:
				bot.send_message(chat_id, "Как часто вы хотите получать новости?", [['Ежедневно'],['Еженедельно']]);
			if status == ConfigurationStatus.WeeklyDigestActivated:
				bot.send_message(chat_id, "Выберите день недели, когда вы хотите получать новости", [config.get("days")]);
			if status == ConfigurationStatus.DailyDigestActivated:
				bot.send_message(chat_id, "Выберите час, в который хотите получать новости. Просто напишите цифру от 0 до 23");
			if status == ConfigurationStatus.Complete:
				bot.send_message(chat_id, "Бот настроен");
		else:
			try:
				command = bot.decode_command(message)
				words = message.split()
				arg = "" if len(words) <= 1 else words[1]
				bot.execute(command, chat_id, arg)
			except KeyError:
				print "Nothing to command"

	return chat

run(host="0.0.0.0", port=os.environ.get('PORT', 5000))