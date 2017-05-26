import urlparse
import urllib
import string
import datetime
import time
import re
import db
from parser import VKParser, RSSParser
from datetime import date, timedelta
from bot import Bot
from config import config

def broadcast_digest(posts, chats):
	feeds = []

	#create feed
	for channel in channels:
		post_feed = ""
		for post in posts:
			if post[0] == channel['name']:
				post_feed += post[1] + "\n\n"
		feeds.append({"name":channel['name'], "text":post_feed})

	# send messages
	if len(feeds) > 0:
		for chat in chats:
			digest_channels = chat[0].split(',') if len(chat[0]) > 0 else []
			for digest_channel in digest_channels:
				for feed in feeds:
					if feed["name"] == digest_channel:
						if len(feed["text"]) > 0:
							bot.broadcast_message(int(chat[1]), str(config.get("report")) + ":\n" + feed["text"])

bot = Bot()
parse_type = str(config.get("type"))
parser = RSSParser() if parse_type =="rss" else VKParser()
channels = config.get("channels");

# FLOW
for channel in channels:
	parser.parse(channel['url'])
	for post in parser.parsed_posts:
		if db.is_post_exist(post['id']) == False:
			db.insert_post(post, channel['name'])
			bot.broadcast_post(post, channel['name'])

# DAILY
current_date = datetime.datetime.fromtimestamp(time.time())
digest_date = db.get_digest_date()[0]
if (current_date > digest_date):
	posts = db.get_posts_between_dates(digest_date - timedelta(hours=24), digest_date)
	chats = db.get_daily_chats()

	broadcast_digest(posts, chats)
	digest_date = digest_date + timedelta(hours=24)
	db.set_digest_date(digest_date, "daily")

# HOURLY
current_date = datetime.datetime.fromtimestamp(time.time())
digest_date = db.get_digest_date()[1]
if (current_date > digest_date):
	posts = db.get_posts_between_dates(digest_date - timedelta(hours=1), digest_date)
	chats = db.get_hourly_chats()

	broadcast_digest(posts, chats)
	digest_date = digest_date + timedelta(hours=1)
	db.set_digest_date(digest_date, "hourly")