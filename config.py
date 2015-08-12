# -*- coding: utf-8 -*-
config = {
    # heroku
    "heroku_postgres_key": "postgres://ocjvdztujmkits:4vMH0a2n7tNh6xzgBPxfnI4rWF@ec2-54-235-134-167.compute-1.amazonaws.com:5432/d48t0kg9fujref",
    "heroku_url": "https://rocky-river-8934.herokuapp.com",

    # telegram
    "telegram_bot_url": "https://api.telegram.org/bot",
    "telegram_token": "119461642:AAFa4t7GQZKRWVAFHb_6xNI76HTSa2FWcns",

    # app
    "type": "vk",
    "hello_message": "Привет!\nЯ бот Хабра, буду присылать уведомления о новых материалах.\n",

    #commands
    "commands":[
        #"search", 
        "/last", 
        "/digest", #(off/on)
        "/flow", #(off/on)
        "/settings",
        "/help"
        ],
    
    "activate_message": "Привет!\nЯ бот Хабра, буду присылать уведомления о новых материалах.",
    "deactivate_message": "Пока!\nЧтобы снова получать от меня уведомления о новых материалах на Хабре, введите команду /start.",

    # vk
    "vk_group_id": "-20629724",

    # days
    "days": [
        'Понедельник'.decode('utf8'),
        'Вторник'.decode('utf8'),
        'Среда'.decode('utf8'),
        'Четверг'.decode('utf8'),
        'Пятница'.decode('utf8'),
        'Суббота'.decode('utf8'),
        'Воскресенье'.decode('utf8')
        ]
}