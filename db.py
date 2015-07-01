# Posts table:
# CREATE SEQUENCE posts_id_seq START 1
# CREATE TABLE public.posts (id   integer   NOT NULL   PRIMARY KEY DEFAULT nextval('posts_id_seq'),external_post_id   integer   NOT NULL   UNIQUE,text TEXT)
#
# Chats table:
# CREATE SEQUENCE chats_id_seq START 1
# CREATE TABLE public.chats (id   integer   NOT NULL   PRIMARY KEY DEFAULT nextval('chats_id_seq'),telegram_chat_id   integer   NOT NULL   UNIQUE)

import psycopg2
import urlparse
from config import config

heroku_key = str(config.get("heroku_postgres_key"))
heroku_url = str(config.get("heroku_url"))

def connect():
	urlparse.uses_netloc.append("postgres")
	url = urlparse.urlparse(heroku_key)
	connection = psycopg2.connect(database = url.path[1:], user = url.username, password = url.password, host = url.hostname, port = url.port)
	return connection

def insert_chat(id):
	if is_chat_exist(id):
		print('Error: Chat already exist')
		return False

	c = connect()
	c.cursor().execute("INSERT INTO chats(id, telegram_chat_id) VALUES(DEFAULT, %s)", [id])
	c.commit()
	c.close()
	print('Chat added')
	return True

def is_chat_exist(id):
	c = connect()
	cursor = c.cursor()
	cursor.execute("SELECT exists(SELECT * FROM chats WHERE telegram_chat_id=%s)", (id,))
	is_exist = cursor.fetchone()[0]
	c.close()
	return is_exist

def get_chats():
	c = connect()
	cursor = c.cursor()
	cursor.execute("SELECT telegram_chat_id FROM chats")
	chats = cursor.fetchall()
	c.close()
	return chats

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