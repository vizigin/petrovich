import feedparser
import cookielib
import urlparse
import urllib2
import urllib
import string
import json
import time
import re
from bot import send_message_all
from db import insert_post
from config import config

API_VK_WALL_GET = "https://api.vk.com/method/wall.get.json?owner_id="
RSS_URL = str(config.get("rss_url"))

parse_type = str(config.get("type"))
owner_id = str(config.get("vk_group_id"))

opener = urllib2.build_opener( urllib2.HTTPCookieProcessor(cookielib.CookieJar()), urllib2.HTTPRedirectHandler())

class Parser:
	def __init__(self):
		self.parsed_posts = []

# Parser for VK Posts
class VKParser(Parser):
	def parse(self, group_id):
		response = opener.open( API_VK_WALL_GET + group_id )
		posts = json.loads(response.read())["response"]
		for post in posts:
			try:
				text = post["text"].replace('<br>', '\n')
				self.parsed_posts.append( {"id":post["id"], "text":text} )
			except TypeError:
				print "Error: Post doesn't have Text or Id"

# Parser for RSS Posts
class RSSParser(Parser):
	def parse(self):
		posts = feedparser.parse( RSS_URL )["entries"]
		for post in posts:
			try:
				title = post["title"]
				link = post["link"]
				description = re.compile(r'<.*?>').sub('', post["description"])
				text = title + "\n\n" + description + "\n\n" + link
				self.parsed_posts.append( {"id":post["guid"], "text":text} )
			except TypeError:
				print "Error: Post doesn't have Text or Id"

def send_posts(posts):
	for post in posts:
		if insert_post(post) == True:
			send_message_all(post["text"])
			time.sleep(5)

if parse_type =="rss":
	parser = RSSParser()
	parser.parse()
else:
	parser = VKParser()
	parser.parse(owner_id)

send_posts(parser.parsed_posts)