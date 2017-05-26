#
#	  WARNING: CALL THIS SCRIPT EVERY WEEK
#

import db
from parser import VKParser, RSSParser
from config import config

parse_type = str(config.get("type"))
parser = RSSParser() if parse_type =="rss" else VKParser()
channels = config.get("channels");
db.clear_cache()

for channel in channels:
	parser.parse(channel['url'])
	for post in parser.parsed_posts:
		if db.is_post_exist(post['id']) == False:
			db.insert_post(post, channel['name'])