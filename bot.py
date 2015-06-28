import os
import psycopg2
import urlparse
import requests
from config import config
from bottle import run, request, post

telegram_bot_url = str(config.get("telegram_bot_url"))
telegram_token = str(config.get("telegram_token"))
heroku_url = str(config.get("heroku_url"))
heroku_key = str(config.get("heroku_postgres_key"))

def init_webhook():
	requests.get( telegram_bot_url + telegram_token + "/setWebhook", params={'url': heroku_url} )

def send_message(userId, text):
	payload = {'chat_id': userId, 'text': text}
	requests.get( telegram_bot_url + telegram_token + "/sendMessage", params=payload )

def insert_user(id):
	urlparse.uses_netloc.append("postgres")
	url = urlparse.urlparse(heroku_key)
	conn = psycopg2.connect(
	    database = url.path[1:],
	    user = url.username,
	    password = url.password,
	    host = url.hostname,
	    port = url.port
	)
	c = conn.cursor()
	
	try:
		c.execute("INSERT INTO users(id, telegram_id) VALUES(DEFAULT, %s)", [id])
		conn.commit()
		conn.close()
		print('Users added')
		return True
	except psycopg2.IntegrityError:
		print('Error: User already exist')
		return False;

@post("/")
def subscribe():
	# todo: error handler
	user_id = request.json['message']['from']['id']
	insert_user(user_id)

run(host="0.0.0.0", port=os.environ.get('PORT', 5000))