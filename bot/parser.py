from config import config
from db import insert_post, is_post_exist
import feedparser 
import urllib2
import json
import cookielib
import urlparse
import re

MAX_POSTS = 10

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
				text = title + "\n" + ("http://" + url.netloc + url.path + "?from=bot")
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
				text = title + "\n" + ("http://" + url.netloc + url.path + "?from=bot")
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
				text = title + "\n" + ("http://" + url.netloc + url.path + "?from=bot")
				print ''.join([i for i in link if i.isdigit()])
				self.parsed_posts.append( {"id":''.join([i for i in link if i.isdigit()]), "text":text} )
				n_posts += 1
				if n_posts == MAX_POSTS:
					return True
			except TypeError:
				print "Error: Post doesn't have Text or Id"
		return True