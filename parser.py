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

login_url = str(config.get("vk_login_url"))
auth_url = str(config.get("vk_auth_url"))

response_type = str(config.get("vk_response_type"))
redirect_uri = str(config.get("vk_redirect_uri"))
client_id = str(config.get("vk_client_id"))
display = str(config.get("vk_display"))
scope = str(config.get("vk_scope"))

password = str(config.get("vk_password"))
email = str(config.get("vk_email"))
group_id = str(config.get("vk_group_id"))

opener = urllib2.build_opener( urllib2.HTTPCookieProcessor(cookielib.CookieJar()), urllib2.HTTPRedirectHandler())

def get_token():
	params = {'client_id': client_id, 'scope': scope, 'redirect_uri': redirect_uri, 'display': display, 'response_type': response_type}
	response = opener.open( auth_url + "?" + urllib.urlencode(params) )
	html = response.read()

	ip_h = re.search(r'ip_h\"\svalue=\"(.*?)\"', html, re.I).group(1)
	lg_h = re.search(r'lg_h\"\svalue=\"(.*?)\"', html, re.I).group(1)
	to = re.search(r'to\"\svalue=\"(.*?)\"', html, re.I).group(1)
	callback_url = auth(ip_h, lg_h, to)

	query = urlparse.parse_qs(urlparse.urlparse(callback_url).fragment)
	return query['user_id'][0], query['access_token'][0]

def auth(ip_h, lg_h, to):
	params = {'act': 'login', 'soft': '1', 'utf8': '1', 'lg_h': lg_h, 'to': to, 'ip_h': ip_h, 'pass': password, '_origin': "http://oauth.vk.com", 'email': email}
	response = opener.open(login_url, urllib.urlencode(params))
	return response.geturl()

def get_posts(group_id):
	response = opener.open( "https://api.vk.com/method/wall.get.json?owner_id=" + str(group_id) )
	json_response = json.loads(response.read())['response']
	return json_response

def save_posts(posts):
	new_posts = []
	for post in posts:
		try:
			post_text = post["text"].replace('<br>', '\n')
			if insert_post(post["id"], post_text) == True:
				new_posts.append(post_text)
		except TypeError:
			print "Error: Post doesn't have texts"
	return new_posts

#user_id, token = get_token()
posts = get_posts(group_id)
new_posts = save_posts(posts)
for text in new_posts:
	send_message_all(text)
	time.sleep(2)