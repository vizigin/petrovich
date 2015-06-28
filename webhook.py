import os
from bottle import run, request, post
from config import config
from db import insert_user

@post("/")
def subscribe():
	# todo: error handler
	user_id = request.json['message']['from']['id']
	insert_user(user_id)

run(host="0.0.0.0", port=os.environ.get('PORT', 5000))