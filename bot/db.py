from datetime import date, timedelta
import psycopg2
import urlparse
import datetime
import logging
import time
from config import config

MAX_DAY_BOUND = 23
MIN_DAY_BOUND = 0
GMT_MOSCOW = 3

heroku_key = str(config.get("heroku_postgres_key"))
heroku_url = str(config.get("heroku_url"))

#
#	  DATABASE
#
def connect():
	urlparse.uses_netloc.append("postgres")
	url = urlparse.urlparse(heroku_key)
	connection = psycopg2.connect(database = url.path[1:], user = url.username, password = url.password, host = url.hostname, port = url.port)
	return connection

def create():
	c = connect()
	c.cursor().execute("CREATE SEQUENCE posts_id_seq START 1")
	c.cursor().execute("CREATE TABLE public.posts (id   bigint   NOT NULL   PRIMARY KEY DEFAULT nextval('posts_id_seq'), external_post_id   bigint   NOT NULL   UNIQUE, text TEXT, date timestamp, type TEXT)")
	c.cursor().execute("CREATE SEQUENCE chats_id_seq START 1")
	c.cursor().execute("CREATE TABLE public.chats (id   bigint   NOT NULL   PRIMARY KEY DEFAULT nextval('chats_id_seq'), telegram_chat_id   bigint   NOT NULL   UNIQUE, auto TEXT DEFAULT '', daily TEXT DEFAULT '', hourly TEXT DEFAULT '')")
	c.cursor().execute("CREATE TABLE public.digest_time (daily timestamp, hourly timestamp)")
	c.commit()
	c.close()

def clear():
	c = connect()
	c.cursor().execute("DROP TABLE public.posts")
	c.cursor().execute("DROP TABLE public.chats")
	c.cursor().execute("DROP TABLE public.digest_time")
	c.cursor().execute("DROP SEQUENCE posts_id_seq")
	c.cursor().execute("DROP SEQUENCE chats_id_seq")
	c.commit()
	c.close()

def clear_cache():
	c = connect()
	c.cursor().execute("DROP TABLE public.posts")
	c.cursor().execute("DROP SEQUENCE posts_id_seq")
	c.commit()
	c.close()

	c = connect()
	c.cursor().execute("CREATE SEQUENCE posts_id_seq START 1")
	c.cursor().execute("CREATE TABLE public.posts (id   bigint   NOT NULL   PRIMARY KEY DEFAULT nextval('posts_id_seq'), external_post_id   bigint   NOT NULL   UNIQUE, text TEXT, date timestamp, type TEXT)")
	c.commit()
	c.close()

#
#	  POSTS
#
def get_random_post():
	c = connect()
	cursor = c.cursor()
	cursor.execute("SELECT COUNT(*) from posts")
	count = cursor.fetchone()[0]
	cursor.execute("SELECT text FROM posts OFFSET random()*" + str(count) + " LIMIT 1;")
	post = cursor.fetchone()[0]
	c.close()
	return post

def insert_post(post, post_type):
	if is_post_exist(post["id"]):
		return False
	ts = time.time()
	current_date = datetime.datetime.fromtimestamp(ts)
	c = connect()
	c.cursor().execute("INSERT INTO posts(id, external_post_id, text, date, type) VALUES(DEFAULT, %s, %s, to_timestamp(%s, 'dd-mm-yyyy hh24:mi:ss'), %s)", (post["id"], post["text"], (current_date.strftime('%d-%m-%Y %H:%M:%S')), post_type))
	c.commit()
	c.close()
	return True

def is_post_exist(id):
	c = connect()
	cursor = c.cursor()
	cursor.execute("SELECT exists(select * from posts where external_post_id=%s)", (id,))
	is_exist = cursor.fetchone()[0]
	c.close()
	return is_exist

def search_posts(word):
	c = connect()
	cursor = c.cursor()
	cursor.execute("SELECT text FROM posts WHERE text ILIKE '%" + word + "%' ORDER BY external_post_id DESC LIMIT 3")
	posts = cursor.fetchall()
	c.close()
	return posts

def get_last_posts(post_type):
	c = connect()
	cursor = c.cursor()
	cursor.execute("SELECT text FROM posts WHERE type=%s ORDER BY external_post_id DESC LIMIT 5", (post_type,))
	posts = cursor.fetchall()
	c.close()
	return posts

def get_posts_between_dates(start_date, end_date):
	c = connect()
	cursor = c.cursor()
	cursor.execute("SELECT type, text FROM posts WHERE date BETWEEN to_timestamp(%s, 'dd-mm-yyyy hh24:mi:ss')::timestamp AND to_timestamp(%s, 'dd-mm-yyyy hh24:mi:ss')::timestamp", (start_date.strftime('%d-%m-%Y %H:%M:%S'), end_date.strftime('%d-%m-%Y %H:%M:%S')))
	posts = cursor.fetchall()
	c.close()
	return posts



#
#	  DIGEST
#
def get_digest_date():
	c = connect()
	cursor = c.cursor()
	cursor.execute("SELECT * FROM digest_time")
	time = cursor.fetchone()
	c.close()
	return time

def set_digest_date(date, type):
	c = connect()
	c.cursor().execute("UPDATE digest_time SET " + type + "=to_timestamp(%s, 'dd-mm-yyyy hh24:mi:ss')", (date.strftime('%d-%m-%Y %H:%M:%S'), ))
	c.commit()
	c.close()

def insert_digest_date(date):
	date = datetime.datetime.fromtimestamp(int(date))
	daily = date.replace(minute=0, second=0)
	hourly = date.replace(minute=0, second=0)

	hour = int(config.get("msk_time_digest"))
	hour = MIN_DAY_BOUND if (hour < MIN_DAY_BOUND) else hour
	hour = MAX_DAY_BOUND if (hour > MAX_DAY_BOUND) else hour
	daily = daily.replace(hour=hour)
	daily = daily - timedelta(hours=GMT_MOSCOW)

	if daily < date:
		daily = daily + datetime.timedelta(days=1)
	
	print daily.strftime('%d-%m-%Y %H:%M:%S')

	c = connect()
	c.cursor().execute("INSERT INTO digest_time(daily, hourly) VALUES(to_timestamp(%s, 'dd-mm-yyyy hh24:mi:ss'), to_timestamp(%s, 'dd-mm-yyyy hh24:mi:ss'))", (daily.strftime('%d-%m-%Y %H:%M:%S'),hourly.strftime('%d-%m-%Y %H:%M:%S')))
	c.commit()
	c.close()

#
#	  CHATS
#
def insert_chat(id):
	c = connect()
	c.cursor().execute("INSERT INTO chats(id, telegram_chat_id) VALUES(DEFAULT, %s)", [id])
	c.commit()
	c.close()
	return True

def is_chat_exist(id):
	c = connect()
	cursor = c.cursor()
	cursor.execute("SELECT exists(SELECT * FROM chats WHERE telegram_chat_id=%s)", (id,))
	is_exist = cursor.fetchone()[0]
	c.close()
	return is_exist

def delete_chat(id):
	c = connect()
	c.cursor().execute("DELETE FROM chats WHERE telegram_chat_id=%s", (id,))
	c.commit()
	c.close()
	return True

def get_daily_chats():
	c = connect()
	cursor = c.cursor()
	cursor.execute("SELECT daily, telegram_chat_id FROM chats")
	chats = cursor.fetchall()
	c.close()
	return chats

def get_hourly_chats():
	c = connect()
	cursor = c.cursor()
	cursor.execute("SELECT hourly, telegram_chat_id FROM chats")
	chats = cursor.fetchall()
	c.close()
	return chats

def get_subscripted_chats(channel):
	c = connect()
	cursor = c.cursor()
	cursor.execute("SELECT telegram_chat_id, auto FROM chats")
	chats = cursor.fetchall()
	c.close()
	subscripted_chats = []
	for chat in chats:
		subscription = chat[1]
		channels = subscription.split(',') if len(subscription) > 0 else []
		for c in channels:
			if c == channel:
				subscripted_chats.append(chat[0])
				break;
	return subscripted_chats

#
#	  CHAT SUBSCRIPTIONS
#
def subscribe_chat(id, channel, subscription_type):
	channels = get_chat_subscriptions(id, subscription_type)
	subscription = ""

	for c in channels:
		if c == channel:
			return False;
		else:
			subscription += c + ','

	subscription += channel
	c = connect()
	c.cursor().execute("UPDATE chats SET " + subscription_type + "=%s WHERE telegram_chat_id=%s", (subscription, id))
	c.commit()
	c.close()
	return True

def unsubscribe_chat(id, channel, subscription_type):
	channels = get_chat_subscriptions(id, subscription_type)
	subscription = ""
	for c in channels:
		if c != channel:
			subscription += c + ','
	subscription = subscription[:-1] if len(subscription) > 0 else subscription

	c = connect()
	c.cursor().execute("UPDATE chats SET " + subscription_type + "=%s WHERE telegram_chat_id=%s", (subscription, id))
	c.commit()
	c.close()
	return True

def get_chat_subscriptions(id, subscription_type):
	c = connect()
	cursor = c.cursor()
	cursor.execute("SELECT " + subscription_type + " FROM chats WHERE telegram_chat_id=%s", [id])
	c.commit()
	subscriptions = cursor.fetchone()[0]
	channels = subscriptions.split(',') if len(subscriptions) > 0 else []
	c.close()
	return channels

def get_chat_subscriptions(id, subscription_type):
	c = connect()
	cursor = c.cursor()
	cursor.execute("SELECT " + subscription_type + " FROM chats WHERE telegram_chat_id=%s", [id])
	c.commit()
	subscriptions = cursor.fetchone()[0]
	channels = subscriptions.split(',') if len(subscriptions) > 0 else []
	c.close()
	return channels