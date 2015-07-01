import os
from bottle import run, request, post
from config import config
from db import insert_chat, get_random_post
from bot import send_message

@post("/")
def subscribe():
	# todo: error handler
	print request.json
	chat_id = request.json['message']['chat']['id']
	result = insert_chat(chat_id)
	if result==True:
		send_message(chat_id, str(config.get("hello_message")))

run(host="0.0.0.0", port=os.environ.get('PORT', 5000))