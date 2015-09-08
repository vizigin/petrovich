#-*- coding: utf-8 -*-
import logging
import config
from db import * 
from enum import Enum
from datetime import date, timedelta

class Type(Enum):
	Stop = "stop"
	Auto = "auto"
	Daily = "daily"
	Hourly = "hourly"

class Chat:
	def __init__(self, chat_id):
		self.chat_id = chat_id;

	def create(self):
		if self.is_exist():
			logging.info("Chat already exist")
			return False
		insert_chat(self.chat_id)
		logging.info("Chat created")
		return True

	def remove(self):
		return delete_chat(self.chat_id)

	def is_exist(self):
		return is_chat_exist(self.chat_id)

	def subscribe(self, channel, subscription_type):
		self.unsubscribe_all(channel);
		channels = config.get("channels");
		for c in channels:
			if c['name'] == channel:
				return subscribe_chat(self.chat_id, channel, subscription_type)
		raise NameError('Такого канала не существует: ' + channel)

	def unsubscribe_all(self, channel):
		self.unsubscribe(channel, Type.Auto)
		self.unsubscribe(channel, Type.Hourly)
		self.unsubscribe(channel, Type.Daily)

	def unsubscribe(self, channel, subscription_type):
		channels = config.get("channels");
		for c in channels:
			if c['name'] == channel and c['forced'] == False:
				return unsubscribe_chat(self.chat_id, channel, subscription_type)
		raise NameError('Такого канала не существует: ' + channel)

	def get_subscriptions(self, subscription_type):
		return get_chat_subscriptions(self.chat_id, subscription_type)

	def get_full_status(self):
		auto = "Подписка: " + self.get_status(Type.Auto)
		daily = "Раз в день: " + self.get_status(Type.Daily)
		hourly = "Раз в час: " + self.get_status(Type.Hourly)
		return auto + "\n" + daily + "\n" + hourly

	def get_status(self, subscription_type):
		subscriptions = self.get_subscriptions(subscription_type)
		channels = config.get("channels");
		status = ""
		for c in channels:
			for s in subscriptions:
				if c['name'] == s and c['forced'] == False:
					status += c['name'] + ','
					break;
		status = status[:-1] if len(status) > 0 else status
		return status