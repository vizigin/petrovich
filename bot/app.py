#-*- coding: utf-8 -*-
from bottle import run, request, post
from config import config
from chat import Chat, Type
from bot import Bot
from db import set_digest_date
import datetime
import logging
import os

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
		channels = config.get("channels");
		for channel in channels:
			chat.subscribe(channel["name"], Type.Auto)
		bot.broadcast_message(chat_id, str(config.get("hello_message")));
		return;
		
	try:
		command = bot.decode_command(message)
		args = message.split()
		args.pop(0)
		bot.execute(command, chat_id, args, date)
	except KeyError:
		print "Nothing to command"
	
	return chat

run(host="0.0.0.0", port=os.environ.get('PORT', 5000))