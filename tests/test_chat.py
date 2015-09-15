#-*- coding: utf-8 -*-
import logging
import datetime
from bot import chat, app, config, db

def test_remove():
	c = chat.Chat(66026064)
	if c.is_exist():
		assert c.remove() == True
	
def test_create():
	c = chat.Chat(66026064)
	if c.is_exist():
		c.remove()
	assert c.create() == True
	c.remove()

def test_configure_subscriptions():
	c = chat.Chat(66026064)
	if c.is_exist():
		c.remove()

	app.process(66026064, "Привет", "1439105337")
	channels = c.get_subscriptions()
	assert channels[0] == "news"
	c.remove()