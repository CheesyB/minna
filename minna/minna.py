#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sqlite3
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from view import View
from dao import Dao
from sql_adapter import SqlAdapter
from config import Config


conf = Config()


def setUpLogging():
    logger = logging.getLogger("minna")
    logger.setLevel(logging.INFO)

    logFormatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s: %(message)s")
    fileHandler = logging.FileHandler("{0}/{1}".format(
        conf.config['LOGPATH'],
        conf.config['LOGNAME']))
    fileHandler.setFormatter(logFormatter)
    fileHandler.setLevel(logging.INFO)
    logger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    consoleHandler.setLevel(logging.INFO)
    logger.addHandler(consoleHandler)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    logger = logging.getLogger("minna.start")
    logger.info("start")
    update.message.reply_text(
        'Hi! Ich bin der Bot:)')


def help(update, context):
    message = "Hallo ich bin der MamuMinnaBot und habe folgende Befehle:\n"\
        "/start\n/help\n/list\n/addList\n/get\n/del\n/add"
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message)




def main():
    setUpLogging()
    logger = logging.getLogger("minna")
    logger.info("started MinnaMamuBot")

    TOKEN = conf.config['TOKEN']
    CONNECTION = conf.config['CONNECTION']
    connection = sqlite3.connect(
        CONNECTION, isolation_level=None, check_same_thread=False)
    adapter = SqlAdapter(connection)
    dao = Dao(adapter)
    view = View(dao)

    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("list", view.all_lists_handler))
    dp.add_handler(CommandHandler("addList", view.add_new_list_handler))
    dp.add_handler(CommandHandler("add", view.add_items_to_list_handler))
    dp.add_handler(CommandHandler("get", view.get_content_handler))
    dp.add_handler(CommandHandler("delList", view.delete_list_handler))
    dp.add_handler(CommandHandler("del", view.delete_items_from_list_handler))
    dp.add_handler(CommandHandler("todo", view.add_sentence_to_list_handler))
    dp.add_handler(CommandHandler(
        "deltodo", view.delete_sentence_from_list_handler))

    # dp.add_handler(MessageHandler(Filter.regex(re.compile(r'^#',)),
    #     view.queryHandler)

    # on noncommand i.e message - echo the message on Telegram

    # log all errors
    dp.add_error_handler(view.error_callback)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
