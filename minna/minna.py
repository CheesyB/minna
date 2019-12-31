#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import sqlite3
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.error import (TelegramError, Unauthorized, BadRequest, 
        TimedOut, ChatMigrated, NetworkError)
from notes import Notes


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)


TOKEN = os.getenv("Minna")


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    logger.info("start")
    update.message.reply_text(
            'Hi! Ich bin der Bot:)')


def help(update, context):
    message = "Hallo ich bin der MamuMinnaBot und habe folgende Befehle:\n"\
            "/start\n/help\n/list\n/addList\n/get\n/del\n/add"
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message)


def error_callback(update, context):
    try:
        raise context.error
    except Unauthorized as e:
        logger.warning(e)
    except BadRequest as e:
        logger.warning(e)
    except TimedOut as e:
        logger.warning(e)
        # handle slow connection problems
    except NetworkError as e:
        logger.warning(e)
        # handle other connection problems
    except ChatMigrated as e:
        logger.warning(e)
        # the chat_id of a group has changed, use e.new_chat_id instead
    except TelegramError as e:
        logger.warning(e)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=str(e))


def main():
    connection = sqlite3.connect(
        ':memory:', isolation_level=None, check_same_thread=False)
    notes = Notes(connection)

    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("list", notes.allListHandler))
    dp.add_handler(CommandHandler("addList", notes.addNewListHandler))
    dp.add_handler(CommandHandler("delList", notes.deleteListHandler))
    dp.add_handler(CommandHandler("get", notes.getContentHandler))
    dp.add_handler(CommandHandler("del", notes.deleteItemsFromListHandler))
    dp.add_handler(CommandHandler("add", notes.addItemsToListHandler))




   # dp.add_handler(MessageHandler(Filter.regex(re.compile(r'^#',)),
   #     notes.queryHandler)

    # on noncommand i.e message - echo the message on Telegram

    # log all errors
    dp.add_error_handler(error_callback)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
