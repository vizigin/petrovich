# Telegram Bot Petrovich
#### Petrovich. Radosti skupyye telegrammy
A [Telegram](https://telegram.org/) bot running with RSS and VK group integration and ready to deploy with Heroku.

### Features
* Bot support commands:
`/last` - send to user last 5 posts 
`/search %search_word%` - send all posts with `%search_word%`
`/random` - send random post
`/off` - turn off auto broadcasting
`/on` - turn on auto broadcasting
`/daily` - turn off daily broadcasting. You can set time in `config.py`
`/hourly` - turn off hourly broadcasting.
`/help` - just send help info
* Bot can work with multiply channels. For example `/last ege` retrieve 5 posts from `ege` channel
* Bot using [botan.io](http://botan.io) for **collecting statistic**.

### Installation
1. [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/vizigin/petrovich)
2. Create the bot on Telegram (just say `/newbot` to [BotFather](https://core.telegram.org/bots#botfather))
3. Update `config.py` with your information (tokens, keys, etc)
4. Uncomment last 2 lines of the `bot.py` script and push all changes to Heroku
5. Run `heroku run python `./bot/bot.py`. It should set new webhook to Heroku server
6. Revert `bot.py` script back and push all changes to Heroku
7. Schedule (I using Heroku Scheduler) VK parser for broadcast posts from your public to users and database cleaner for long support. I use `python ./bot/broadcaster.py` every 10 minutes for Brodcaster and `if [ "$(date +%d)" = 01 ]; then python ./bot/cache_cleaner.py; fi` for Database Cleaner
8. That's it!

This repo used by: 
* [Banekbot](http://telegram.me/banekbot). Bot for VK [public](https://vk.com/baneks)
* [SMMRussiabot](http://telegram.me/smmrussiabot). Bot for RSS [site](http://siliconrus.com)
* [EchoMSK](https://telegram.me/echom_bot). Bot for RSS [site](http://echo.msk.ru/)
* [Diletant](https://telegram.me/diletant_bot). Bot for RSS [site](http://diletant.media/)
* [iGuides](https://telegram.me/iGuidesBot). Bot for RSS [site](iguides.ru)