#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import MessageHandler, Filters
from telegram.error import TelegramError
from sql_adapter import SqlAdapter
import pprint
import datetime
import logging
import re


logger = logging.getLogger(__name__)


def convertTs(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%d.%m.%Y')


def cpp(liste):
    result = ''
    for i, row in enumerate(liste):
        result += '{}. {} \n'.format(i+1, row[0])
    return result


class Notes(object):

    def __init__(self, connection):
        self.adapter = SqlAdapter(connection)
        self.logger = logging.getLogger(__name__)

    def allListHandler(self, update, context):
        allLists = self.adapter.allLists
        if not allLists:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Tia, keine Listen angelegt:)")
        filteredList = [
            [row[1], convertTs(row[2])]
            for row in allLists
        ]
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=cpp(filteredList))

    def addNewListHandler(self, update, context):
        if context.args:
            tag = context.args[0]
            self.adapter.newList(tag)
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="neue List {}".format(tag))
        else:
            raise TelegramError("Wie soll denn die neue Liste heißen?")

    def getContentHandler(self, update, context):
        if context.args:
            tag = context.args[0]
            try:
                items = self.adapter.getContent(tag)
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=cpp(items))
                return
            except Exception as e:
                self.logger.info(" getContentHandler error: {}", e)
                raise TelegramError('Hups ein Fehler: gibts die '
                                    'Liste {} wirklich?'.format(tag))
        else:
            raise TelegramError("Welche Liste soll ich ausgeben?")

    def deleteItemsFromListHandler(self, update, context):
        if not len(context.args) >= 2:
            raise TelegramError("Zu wenig infos?")
        tag = context.args[0]
        message = 'Gelöscht von {}: '.format(tag)
        for item in context.args[1:]:
            self.adapter.deleteItemFromList(item, tag)
            message += '{} '.format(item)
        message += '\n {}'.format(cpp(self.adapter.getContent(tag)))
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message)

    def addItemsToListHandler(self, update, context):
        if not len(context.args) >= 2:
            raise TelegramError("Zu wenig infos?")
        tag = context.args[0]
        self.adapter.addItemsToList(context.args[1:], tag)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=cpp(self.adapter.getContent(tag)))

    def deleteListHandler(self, update, context):
        if not context.args:
            raise TelegramError("Welche Liste soll ich löschen?")
        tag = context.args[0]
        try:
            self.adapter.deleteList(context.args[0])
        except Exception as e:
            raise TelegramError("Die Liste {} gibt es wohl"
                                "nicht:(".format(tag))

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Liste {} gelöscht".format(tag))
