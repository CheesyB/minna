#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import MessageHandler, Filters
from telegram.error import TelegramError
from dao import Dao
import pprint
import datetime import logging
import re


def cpp(liste):
    result = ''
    for i, row in enumerate(liste):
        result += '{}. {} \n'.format(i+1, row[0])
    return result


class View(object):

    def __init__(self, dao):
        self.logger = logging.getLogger(__name__)
        self.dao = dao

    def send(self, context, update, message):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message)

    def convert_ts(self, timestamp):
        return datetime.datetime.fromtimestamp(timestamp).strftime('%d.%m.%Y')

    def _check_raise_args(self, args, error_msg):
        if args:
            return args
        else:
            raise TelegramError(error_msg)

    def all_list_handler(self, update, context):
        allLists = self.dao.allLists
        if not allLists:
            self.send(update, context, "Tia keine Liste angelegt")

        filteredList = [
            [row[1], self.convertTs(row[2])]
            for row in allLists
        ]
        self.send(update, context, cpp(filteredList))

    def add_new_list_handler(self, update, context):
        args = self._check_raise_args(context.args,
                                   "Wie soll denn die Liste heißen?")
        tag = args[0]
        self.dao.newList(tag)
        self.send(update, context, "neue List {}".format(tag))

    def get_content_handler(self, update, context):
        args = self._check_raise_args(context.args,
                                   "Welche Liste soll ich ausgeben?")
        tag = args[0]
        try:
            items = self.adapter.getContent(tag)
            self.send(update, context, cpp(items))
        except Exception as e:
            self.logger.info(" getContentHandler error: {}", e)
            raise TelegramError('Hups ein Fehler: gibts die '
                                'Liste {} wirklich?'.format(tag))

    def delete_items_from_list_handler(self, update, context):
        if not len(context.args) >= 2:
            raise TelegramError("Zu wenig infos?")
        tag = context.args[0]
        message = 'Gelöscht von {}: '.format(tag)
        for item in context.args[1:]:
            self.dao.deleteItemFromList(item, tag)
            message += '{} '.format(item)
        message += '\n {}'.format(cpp(self.adapter.getContent(tag)))
        self.send(update, context, message)

    def add_items_to_list_handler(self, update, context):
        if not len(context.args) >= 2:
            raise TelegramError("Zu wenig infos?")
        tag = context.args[0]
        self.dao.addItemsToList(context.args[1:], tag)
        self.send(update, context, cpp(self.dao.getContent(tag)))

    def delete_list_handler(self, update, context):
        self._check_raise_args(context.args, "Welche Liste soll ich löschen?")
        tag = context.args[0]
        try:
            self.adapter.deleteList(context.args[0])
        except Exception as e:
            raise TelegramError("Die Liste {} gibt es wohl"
                                "nicht:(".format(tag))
        self.send(update, context, "Liste {} gelöscht".format(tag))




