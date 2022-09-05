# -*- coding: utf-8 -*-

config = {
    # heroku
    "heroku_postgres_key": "postgres://josdegmknehgev:fbe0f6a3d4659862376e8c3c7b8c3f99c5bf81ae4e0235feb58a162b895c7aeb@ec2-34-247-72-29.eu-west-1.compute.amazonaws.com:5432/d72nk3fl871u4c",
    "heroku_url": "https://wldnr-vk-tg-bot.herokuapp.com/",

    # telegram
    "telegram_bot_url": "https://api.telegram.org/bot",
    "telegram_token": "5546855722:AAGCPEUGQa4wiBrN0AGLMvPYVwhe37GxJ-I",

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
