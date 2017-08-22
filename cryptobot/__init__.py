#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simple telegram bot to have crypto currencies prices from cryptowatch.ch
"""

from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler
import logging
import requests
import json

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

URL = "https://api.cryptowat.ch/markets/{market}/{base}{quote}/summary"

def price(bot, update):
    # Default values
    market = "gdax"
    base = "btc"
    quote = "usd"

    token = update.message.text.split()

    if len(token) > 1:
        base = token[1]
    if len(token) > 2:
        quote = token[2]
    if len(token) > 3:
        market = token[3]

    url = URL.replace("{market}", market).replace("{base}", base).replace("{quote}", quote)

    res = requests.get(url)
    # print(res)
    if res.ok:
        jsonData = json.loads(res.content)["result"]
        price = jsonData["price"]
        update.message.reply_text("Price: *%s* (high: %s, low: %s, percentage: %s%%, volume: %s)" % (price["last"], price["high"], price["low"], price["change"]["percentage"], jsonData["volume"]),
                                  parse_mode=ParseMode.MARKDOWN)
    else:
        update.message.reply_text("Something is wrong")
        logger.warn('Query "%s" caused error "%s"' % (URL, res.raise_for_status()))


def help(bot, update):
    update.message.reply_text('/price <base> (<quote>) (<market>)')


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # EventHandler
    updater = Updater("TOKEN")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands
    dp.add_handler(CommandHandler("price", price))
    dp.add_handler(CommandHandler("help", help))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
