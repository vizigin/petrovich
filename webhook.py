# -*- coding: utf-8 -*-

import os
from bot import Bot
from bottle import run, request, post
from config import config
from db import insert_chat, get_random_post, is_active

bot = Bot()

@post("/")
def subscribe():
	# todo: error handler
	chat_id = request.json['message']['chat']['id']

	try:
		command_text = parse_command(request.json['message']['text'])
		bot.execute(command_text, chat_id)
		return;
	except KeyError:
		print "Nothing to command"

	if is_active(chat_id):
		if insert_chat(chat_id):
			bot.send_message(chat_id, str(config.get("hello_message")))
		else:
			bot.send_message(chat_id, "Вот тебе баян:\n" + get_random_post()) 

def parse_command(text):
	if text.find( str(config.get("activate_command")) ) != -1: 
		return str(config.get("activate_command"))
	if text.find( str(config.get("deactivate_command")) ) != -1: 
		return str(config.get("deactivate_command"))
	raise KeyError('Commands not found')

run(host="0.0.0.0", port=os.environ.get('PORT', 5000))