# Telegram Bot Petrovich
#### Petrovich. Radosti skupyye telegrammy
A [Telegram](https://telegram.org/) bot running with RSS and VK group integration and ready to deploy with Heroku.
Now bot supports sending text message from RSS and VK groups only.

### Installation
1. Clone this repo
2. `pip install -r requirements.txt`
3. Create the bot on Telegram (just say `/newbot` to [BotFather](https://core.telegram.org/bots#botfather))
4. Update `config.py` with your information (tokens, keys, etc)
5. For first run you should uncomment `init_webhook()` and run `python bot.py`. It should set new webhook to Heroku server
6. For broadcast message from your VK public just run `python parser.py`. It retrieves 20 post and sends it to all user of Heroku database
7. That's it!

### Heroku
You can host your Bot for free on [Heroku](http://heroku.com). It is ready to deploy.

```bash
heroku create
git push heroku master
heroku ps:scale web=1
heroku ps
heroku logs
```

Also you should schedule (I using Heroku Scheduler) VK parser for broadcast posts from your public to users.

This repo used by: 
* [Banekbot](http://telegram.me/banekbot). Bot for VK [public](https://vk.com/baneks)
* [SMMRussiabot](http://telegram.me/smmrussiabot). Bot for RSS [site](http://siliconrus.com)
* [iGuidesbot](https://telegram.me/iguidesbot). Bot for RSS [site](https://www.iguides.ru/)
