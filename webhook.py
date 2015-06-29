#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import os
from bottle import run, request, post
from config import config
from db import insert_user
from bot import send_message

@post("/")
def subscribe():
	# todo: error handler
	user_id = request.json['message']['from']['id']
	result = insert_user(user_id)
	if result==True:
		send_message(user_id, "Привет, любимый! Я буду присылать тебе свежие анекдоты категории Б по мере их появления в сообществе vk.com/baneks")
	else:
		send_message(user_id, "Пока мне нечего тебе ответить.\nКак будет новый анекдот — пришлю.")


run(host="0.0.0.0", port=os.environ.get('PORT', 5000))