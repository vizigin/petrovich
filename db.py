# Posts table:
# CREATE SEQUENCE posts_id_seq START 1
# CREATE TABLE public.posts (id   integer   NOT NULL   PRIMARY KEY DEFAULT nextval('posts_id_seq'),vkpost_id   integer   NOT NULL   UNIQUE,text TEXT)
#
# Users table:
# CREATE SEQUENCE users_id_seq START 1
# CREATE TABLE public.users (id   integer   NOT NULL   PRIMARY KEY DEFAULT nextval('users_id_seq'),telegram_id   integer   NOT NULL   UNIQUE)

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

def insert_user(id):
	c = connect()
	try:
		c.cursor().execute("INSERT INTO users(id, telegram_id) VALUES(DEFAULT, %s)", [id])
		c.commit()
		c.close()
		print('Users added')
		return True
	except psycopg2.IntegrityError:
		c.close()
		print('Error: User already exist')
		return False;
	
def get_users():
	c = connect()
	cursor = c.cursor()
	cursor.execute("SELECT telegram_id FROM users")
	users = cursor.fetchall()
	c.close()
	return users

def insert_post(vkpost_id, text):
	c = connect()
	try:
		c.cursor().execute("INSERT INTO posts(id, vkpost_id, text) VALUES(DEFAULT, %s, %s)", (vkpost_id, text))
		c.commit()
		c.close()
		print('Post added')
		return True
	except psycopg2.IntegrityError:
		c.close()
		print('Error: Post already exist')
		return False;
