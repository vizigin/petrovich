# -*- coding: utf-8 -*-

config = {
    # heroku
    "heroku_postgres_key": "<here your postgres url>",
    "heroku_url": "<heroku url>",

    # telegram
    "telegram_bot_url": "https://api.telegram.org/bot",
    "telegram_token": "<telegram bot token>",

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
        "/off",
        "/on",
        "/daily",
        "/hourly",
        "/help"
        ],

    #yandex. metrika
    "ya_token": "<Yandex.Metrika code>",
   
    "doesntexist_message": "Channel doesn't exist",
    "report": "Report header",
    "auto_message": "Subscribed",
    "auto_error": "Already subscribed",
    "stop_message": "Unsubscribed",
    "hourly_message": "Hourly subscribed",
    "daily_message": "Daily subscribed",
    "msk_time_digest": "20", 

    "subscribe_message": "<SUBSCRIBED MESSAGE>",
    "last_message": "<LAST MESSAGE>",
    "hello_message": "<HELLO MESSAGE>"
}