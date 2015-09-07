# -*- coding: utf-8 -*-

config = {
    # heroku
    "heroku_postgres_key": "<here your postgres token>",
    "heroku_url": "https://upper-syrup-2282.herokuapp.com",

    # telegram
    "telegram_bot_url": "https://api.telegram.org/bot",
    "telegram_token": "<here your bot token>",

    # app
    "type": "vk",
    "channels":[ 
        {"name" : "basic", "url" : "https://api.vk.com/method/wall.get.json?owner_id=-1", 'forced': False}
    ],

    #commands
    "commands":[ 
        "/last", 
        "/search", 
        "/random",
        "/subscribe",
        "/help"
        ],
   
    "doesntexist_message": "Channel doesn't exist",
    "auto_message": "Subscribed",
    "auto_error": "Already subscribed",
    "stop_message": "Unsubscribed",
    "stop_error": "Already unsubscribed",
    "digest_message": "Digest subscribed",
    "digest_error": "Already subscribed",
    "msk_time_digest": "20", 

    "subscribe_message": "<SUBSCRIBED MESSAGE>",
    "last_message": "<LAST MESSAGE>",
    "hello_message": "<HELLO MESSAGE>",
    "help_message": "<HELP MESSAGE>"
}