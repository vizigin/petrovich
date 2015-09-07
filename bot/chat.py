#-*- coding: utf-8 -*-
import logging
import config
from db import * 
from enum import Enum
from datetime import date, timedelta

MAX_DAY_BOUND = 23
MIN_DAY_BOUND = 0
DAYS_IN_WEEK = 7
GMT_MOSCOW = 3

class Status(Enum):
	Stop = "stop"
	Auto = "auto"
	Digest = "digest"

class Type(Enum):
	Subscription = "subscription"
	Digest = "digest"

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
		unsubscription_type = Type.Subscription if subscription_type == Type.Digest else Type.Digest
		self.unsubscribe(channel, unsubscription_type)

		channels = config.get("channels");
		for c in channels:
			if c['name'] == channel:
				return subscribe_chat(self.chat_id, channel, subscription_type)
		raise NameError('Такого канала не существует: ' + channel)

	def unsubscribe(self, channel, subscription_type):
		channels = config.get("channels");
		for c in channels:
			if c['name'] == channel and c['forced'] == False:
				return unsubscribe_chat(self.chat_id, channel, subscription_type)
		raise NameError('Такого канала не существует: ' + channel)

	def get_subscriptions(self, subscription_type):
		return get_chat_subscriptions(self.chat_id, subscription_type)

	def get_full_status(self):
		subscriptions = "Подписка: " + self.get_status(Type.Subscription)
		digest = "Дайджест: " + self.get_status(Type.Digest)
		return subscriptions + "\n" + digest

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