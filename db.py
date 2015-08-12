# Posts table:
# CREATE SEQUENCE posts_id_seq START 1
# CREATE TABLE public.posts (id   integer   NOT NULL   PRIMARY KEY DEFAULT nextval('posts_id_seq'),external_post_id   integer   NOT NULL   UNIQUE,text TEXT)
#
# Chats table:
# CREATE SEQUENCE chats_id_seq START 1
# CREATE TYPE digest AS ENUM ('None', 'Daily', 'Weekly');
# CREATE TYPE flow AS ENUM ('None', 'Flow');
# CREATE TABLE public.chats (id   integer   NOT NULL   PRIMARY KEY DEFAULT nextval('chats_id_seq'),telegram_chat_id   integer   NOT NULL   UNIQUE, is_configured BOOL DEFAULT FALSE, flow_mode flow DEFAULT 'None', digest_mode digest DEFAULT 'None', next_digest_date timestamp)
#

import psycopg2
import urlparse
import time
import datetime
import logging
from config import config

heroku_key = str(config.get("heroku_postgres_key"))
heroku_url = str(config.get("heroku_url"))

def connect():
	urlparse.uses_netloc.append("postgres")
	url = urlparse.urlparse(heroku_key)
	connection = psycopg2.connect(database = url.path[1:], user = url.username, password = url.password, host = url.hostname, port = url.port)
	return connection

def get_random_post():
	c = connect()
	cursor = c.cursor()
	cursor.execute("SELECT COUNT(*) from posts")
	count = cursor.fetchone()[0]
	cursor.execute("SELECT text FROM posts OFFSET random()*" + str(count) + " LIMIT 1;")
	post = cursor.fetchone()[0]
	c.close()
	return post

def insert_post(post):
	if is_post_exist(post["id"]):
		print('Error: Post already exist')
		return False

	c = connect()
	c.cursor().execute("INSERT INTO posts(id, external_post_id, text) VALUES(DEFAULT, %s, %s)", (post["id"], post["text"]))
	c.commit()
	c.close()
	print('Post added')
	return True

def is_post_exist(id):
	c = connect()
	cursor = c.cursor()
	cursor.execute("SELECT exists(select * from posts where external_post_id=%s)", (id,))
	is_exist = cursor.fetchone()[0]
	c.close()
	return is_exist


#
#	  CHATS
#	* Check exist
#	* Insert
#	* Delete
#
def get_chats():
	c = connect()
	cursor = c.cursor()
	cursor.execute("SELECT telegram_chat_id FROM chats WHERE active=True")
	chats = cursor.fetchall()
	c.close()
	return chats

def is_chat_exist(id):
	c = connect()
	cursor = c.cursor()
	cursor.execute("SELECT exists(SELECT * FROM chats WHERE telegram_chat_id=%s)", (id,))
	is_exist = cursor.fetchone()[0]
	c.close()
	return is_exist

def insert_chat(id):
	c = connect()
	c.cursor().execute("INSERT INTO chats(id, telegram_chat_id) VALUES(DEFAULT, %s)", [id])
	c.commit()
	c.close()
	return True

def delete_chat(id):
	c = connect()
	c.cursor().execute("DELETE FROM chats WHERE telegram_chat_id=%s", (id,))
	c.commit()
	c.close()
	return True

def is_chat_configured(id):
	c = connect()
	cursor = c.cursor()
	cursor.execute("SELECT is_configured FROM chats WHERE telegram_chat_id=%s", [id])
	c.commit()
	is_configured = cursor.fetchone()[0]
	c.close()
	return is_configured

def configure_chat(id):
	c = connect()
	c.cursor().execute("UPDATE chats SET is_configured=TRUE WHERE telegram_chat_id=%s", [id])
	c.commit()
	c.close()

def deconfigure_chat(id):
	c = connect()
	c.cursor().execute("UPDATE chats SET is_configured=FALSE WHERE telegram_chat_id=%s", [id])
	c.commit()
	c.close()

#	CHAT MODES
def get_chat_flow_mode(id):
	c = connect()
	cursor = c.cursor()
	cursor.execute("SELECT flow_mode FROM chats WHERE telegram_chat_id=%s", [id])
	c.commit()
	flow_mode = cursor.fetchone()[0]
	c.close()
	return flow_mode

def set_chat_flow_mode(id, mode):
	c = connect()
	c.cursor().execute("UPDATE chats SET flow_mode=%s WHERE telegram_chat_id=%s", (mode, id))
	c.commit()
	c.close()

def get_chat_digest_mode(id):
	c = connect()
	cursor = c.cursor()
	cursor.execute("SELECT digest_mode FROM chats WHERE telegram_chat_id=%s", [id])
	c.commit()
	digest_mode = cursor.fetchone()[0]
	c.close()
	return digest_mode

def set_chat_digest_mode(id, mode):
	c = connect()
	c.cursor().execute("UPDATE chats SET digest_mode=%s WHERE telegram_chat_id=%s", (mode, id))
	c.commit()
	c.close()

def get_chat_digest_date(id):
	c = connect()
	cursor = c.cursor()
	cursor.execute("SELECT next_digest_date FROM chats WHERE telegram_chat_id=%s", [id])
	c.commit()
	next_digest_date = cursor.fetchone()[0]
	c.close()
	return next_digest_date

def set_chat_digest_date(id, date):
	c = connect()
	c.cursor().execute("UPDATE chats SET next_digest_date=to_timestamp(%s, 'dd-mm-yyyy hh24:mi:ss') WHERE telegram_chat_id=%s", (date.strftime('%d-%m-%Y %H:%M:%S'), id))
	c.commit()
	c.close()