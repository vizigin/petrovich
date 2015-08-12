#-*- coding: utf-8 -*-
import logging
import datetime
from db import * 
from enum import Enum

MAX_DAY_BOUND = 23
MIN_DAY_BOUND = 0
DAYS_IN_WEEK = 7

class ConfigurationStatus(Enum):
	NoStatus = 0
	WeeklyDigestActivated = 1
	DailyDigestActivated = 2
	DigestActivated = 3
	Complete = 4

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
	
	def configure(self, message, date):
		if self.is_configure():
			logging.info("Chat already configured")
			return False

		date_of_message = datetime.datetime.fromtimestamp(int(date))
		status = self.set_mode(message)
		if status != ConfigurationStatus.NoStatus:
			return status

		status = self.set_digest_date(message, date_of_message)
		return status

	def deconfigure(self):
		if self.is_exist() == False:
			logging.error("Chat doesn't exist")
			return False

		deconfigure_chat(self.chat_id)
		logging.info("Chat deconfigured")
		return False

	def is_configure(self):
		return is_chat_configured(self.chat_id)

	def set_flow_mode(self, value):
		set_chat_flow_mode(self.chat_id, value)

	def get_mode_config(self):
		return {
			'flow' : get_chat_flow_mode(self.chat_id), 
			'digest' : get_chat_digest_mode(self.chat_id)
			}

	def set_mode(self, message):
		if message == "Дайджест".decode('utf8') and self.get_mode_config()['digest'] == 'None':
			return ConfigurationStatus.DigestActivated

		if message == "Поток".decode('utf8'):
			self.set_flow_mode('Flow')
			configure_chat(self.chat_id)
			return ConfigurationStatus.Complete

		if message == "Еженедельно".decode('utf8'):
			set_chat_digest_mode(self.chat_id, 'Weekly')
			return ConfigurationStatus.WeeklyDigestActivated

		if message == "Ежедневно".decode('utf8'):
			set_chat_digest_mode(self.chat_id, 'Daily')
			return ConfigurationStatus.DailyDigestActivated

		return ConfigurationStatus.NoStatus

	def set_digest_date(self, message, date):
		status = ConfigurationStatus.NoStatus
		if get_chat_digest_mode(self.chat_id) == 'Weekly':
			status = self.set_digest_day(message, date)
		status = self.set_digest_hour(message, date) if status == ConfigurationStatus.NoStatus else status
		return status
		
	def set_digest_day(self, message, date):
		nday = 0
		digest_date = date.replace(minute=0, second=0)
		for day in config.get("days"):
			if day == message:
				current_weekday = date.weekday()
				offset = nday - current_weekday if nday >= current_weekday else DAYS_IN_WEEK - (current_weekday - nday)
				digest_date = digest_date + datetime.timedelta(days=offset)
				set_chat_digest_date(self.chat_id, digest_date)
				return ConfigurationStatus.DailyDigestActivated
			nday = nday + 1
		return ConfigurationStatus.NoStatus

	def set_digest_hour(self, message, date):
		digest_date = get_chat_digest_date(self.chat_id) if get_chat_digest_mode(self.chat_id) == 'Weekly' else date.replace(minute=0, second=0)
		try:
			hour = int(message)
			hour = MIN_DAY_BOUND if (hour < MIN_DAY_BOUND) else hour
			hour = MAX_DAY_BOUND if (hour > MAX_DAY_BOUND) else hour
			digest_date = digest_date.replace(hour=hour)

			if digest_date < date:
				digest_date = digest_date + datetime.timedelta(days=1)
			set_chat_digest_date(self.chat_id, digest_date)
			configure_chat(self.chat_id)
			return ConfigurationStatus.Complete
		except ValueError:
			return ConfigurationStatus.NoStatus;
		except AttributeError:
			return ConfigurationStatus.NoStatus;

	def get_digest_date(self):
		return get_chat_digest_date(self.chat_id)