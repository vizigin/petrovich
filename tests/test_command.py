#-*- coding: utf-8 -*-
from bot import chat, app
import logging
import time

# Должен присылать инфу о хелпе
def test_help_command():
	c = chat.Chat(66026064)
	if c.is_exist():
		c.remove()
	app.process(66026064, "Привет", "1439105337")
	app.process(66026064, "/help", "1438600337")
	c.remove()
	time.sleep(30)

def test_last_command():
	c = chat.Chat(66026064)
	if c.is_exist():
		c.remove()
	app.process(66026064, "Привет", "1439105337")
	app.process(66026064, "/last", "1438600337")
	c.remove()
	time.sleep(30)

# Должен выслать 5 последних новостей
def test_last_news_command():
	c = chat.Chat(66026064)
	if c.is_exist():
		c.remove()
	app.process(66026064, "Привет", "1439105337")
	app.process(66026064, "/last news", "1438600337")
	c.remove()
	time.sleep(30)

# Должен выслать 5 последних блогов
def test_last_blogs_command():
	c = chat.Chat(66026064)
	if c.is_exist():
		c.remove()
	app.process(66026064, "Привет", "1439105337")
	app.process(66026064, "/last blogs", "1438600337")
	c.remove()
	time.sleep(30)

def test_random_command():
	c = chat.Chat(66026064)
	if c.is_exist():
		c.remove()
	app.process(66026064, "Привет", "1439105337")
	app.process(66026064, "/random", "1438600337")
	c.remove()
	time.sleep(30)

def test_search_command():
	c = chat.Chat(66026064)
	if c.is_exist():
		c.remove()
	app.process(66026064, "Привет", "1439105337")
	app.process(66026064, "/search а", "1438600337")
	c.remove()
	time.sleep(30)

def test_subscribe_command():
	c = chat.Chat(66026064)
	if c.is_exist():
		c.remove()
	app.process(66026064, "Привет", "1439105337")
	app.process(66026064, "/subscribe", "1438600337")
	c.remove()
	time.sleep(30)

def test_subscribe_news_stop_command():
	c = chat.Chat(66026064)
	if c.is_exist():
		c.remove()
	app.process(66026064, "Привет", "1439105337")
	app.process(66026064, "/subscribe news stop", "1438600337")
	app.process(66026064, "/subscribe", "1438600337")
	app.process(66026064, "/subscribe news auto", "1438600337")
	c.remove()
	time.sleep(30)

def test_subscribe_news_auto_command():
	c = chat.Chat(66026064)
	if c.is_exist():
		c.remove()
	app.process(66026064, "Привет", "1439105337")
	app.process(66026064, "/subscribe news auto", "1438600337")
	c.remove()
	time.sleep(30)

def test_subscribe_unknown_command():
	c = chat.Chat(66026064)
	if c.is_exist():
		c.remove()
	app.process(66026064, "Привет", "1439105337")
	app.process(66026064, "/subscribe test auto", "1438600337")
	c.remove()
	time.sleep(30)

def test_unsubscribe_unknown_command():
	c = chat.Chat(66026064)
	if c.is_exist():
		c.remove()
	app.process(66026064, "Привет", "1439105337")
	app.process(66026064, "/subscribe test stop", "1438600337")
	c.remove()

def test_subscribe_digest_command():
	c = chat.Chat(66026064)
	if c.is_exist():
		c.remove()
	app.process(66026064, "Привет", "1439105337")
	app.process(66026064, "/subscribe digest", "1438600337")
	app.process(66026064, "/subscribe", "1438600337")
	#c.remove()