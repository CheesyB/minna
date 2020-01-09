#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import sqlite3
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.error import (TelegramError, Unauthorized, BadRequest,
                            TimedOut, ChatMigrated, NetworkError)
from view import View
from dao import Dao
from sql_adapter import SqlAdapter


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)




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
    TOKEN = os.getenv("TOKEN")
    CONNECTION = os.getenv("CONNECTION")
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
    dp.add_handler(CommandHandler("deltodo", view.delete_sentence_from_list_handler))

   # dp.add_handler(MessageHandler(Filter.regex(re.compile(r'^#',)),
   #     view.queryHandler)

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
