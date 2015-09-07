#-*- coding: utf-8 -*-

import feedparser
import cookielib
import urlparse
import urllib2
import urllib
import string
import json
import datetime
from datetime import date, timedelta
import time
import re
from bot import Bot
from config import config
from db import insert_post, is_post_exist, get_digest_date, get_posts_last_24_hour, get_digest_chats, set_digest_date

MAX_POSTS = 10
parse_type = str(config.get("type"))

opener = urllib2.build_opener( urllib2.HTTPCookieProcessor(cookielib.CookieJar()), urllib2.HTTPRedirectHandler())

class Parser:
	def __init__(self):
		self.parsed_posts = []

# Parser for VK Posts
class VKParser(Parser):
	def parse(self, url):
		response = opener.open(url)
		posts = json.loads(response.read())["response"]
		for post in posts:
			try:
				text = post["text"].replace('<br>', '\n')
				self.parsed_posts.append( {"id":post["id"], "text":text} )
			except TypeError:
				print "Error: Post doesn't have Text or Id"

# Parser for RSS Posts
class RSSParser(Parser):
	def parse(self, url):
		# http://echo.msk.ru/export/yandex_rss2.xml
		result = self.parse_yandex_rss(url)
		if result == True: 
			return;
		# http://echo.msk.ru/blog/rss.xml
		result = self.parse_echo_rss(url)
		if result == True: 
			return;

		result = self.parse_diletant_rss(url)
		if result == True: 
			return;

	def parse_yandex_rss(self, url):
		posts = feedparser.parse( url )["entries"]
		n_posts = 0
		for post in posts:
			try:
				title = post["title"]
				link = post["link"]
				url = urlparse.urlparse(link)
				description = re.compile(r'<.*?>').sub('', post["yandex_full-text"])
				text = title + "\n" + (url.netloc + url.path + "?from=bot")
				self.parsed_posts.append( {"id":''.join([i for i in link if i.isdigit()]), "text":text} )
				n_posts += 1
				if n_posts == MAX_POSTS:
					return True
			except TypeError:
				print "Error: Post doesn't have Text or Id"
			except KeyError:
				return False
		return True

	def parse_echo_rss(self, url):
		posts = feedparser.parse( url )["entries"]
		n_posts = 0
		for post in posts:
			try:
				title = post["title"]
				link = post["link"]
				guid = post["guid"]
				url = urlparse.urlparse(link)
				description = re.compile(r'<.*?>').sub('', post["description"])
				text = title + "\n\n" + (url.netloc + url.path + "?from=bot")
				self.parsed_posts.append( {"id":''.join([i for i in guid if i.isdigit()]), "text":text} )
				n_posts += 1
				if n_posts == MAX_POSTS:
					return True
			except TypeError:
				print "Error: Post doesn't have Text or Id"
			except KeyError:
				return False
		return True

	def parse_diletant_rss(self, url):
		posts = feedparser.parse( url )["entries"]
		n_posts = 0
		print url
		for post in posts:
			try:
				title = post["title"]
				link = post["link"]
				url = urlparse.urlparse(link)
				description = re.compile(r'<.*?>').sub('', post["description"])
				text = title + "\n\n" + (url.netloc + url.path + "?from=bot")
				print ''.join([i for i in link if i.isdigit()])
				self.parsed_posts.append( {"id":''.join([i for i in link if i.isdigit()]), "text":text} )
				n_posts += 1
				if n_posts == MAX_POSTS:
					return True
			except TypeError:
				print "Error: Post doesn't have Text or Id"
		return True

bot = Bot()
parser = RSSParser() if parse_type =="rss" else VKParser()
channels = config.get("channels");

# FLOW
for channel in channels:
	parser.parse(channel['url'])
	for post in parser.parsed_posts:
		if is_post_exist(post['id']) == False:
			insert_post(post, channel['name'])
			bot.broadcast_post(post, channel['name'])

# DIGEST
current_date = datetime.datetime.fromtimestamp(time.time())
digest_date = get_digest_date()
if (current_date > digest_date):
	posts = get_posts_last_24_hour(digest_date)
	feeds = []
	
	#create feed
	for channel in channels:
		post_feed = ""
		for post in posts:
			if post[0] == channel['name']:
				post_feed += post[1] + "\n"
		feeds.append({"name":channel['name'], "text":post_feed})

	# send messages
	chats = get_digest_chats()
	for chat in chats:
		digest_channels = chat[0].split(',') if len(chat[0]) > 0 else []
		for digest_channel in digest_channels:
			for feed in feeds:
				if feed["name"] == digest_channel:
					bot.broadcast_message(int(chat[1]), "Сводка новостей по рубрике за день:\n" + feed["text"])

	digest_date = digest_date + timedelta(hours=24)
	set_digest_date(digest_date)