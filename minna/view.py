#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import MessageHandler, Filters
from telegram.error import TelegramError
from dao import Dao
import pprint
import functools
import datetime
import logging
import re


def send(func):
    @functools.wraps(func)
    def wrapper_send(*args, **kwargs):
        message = func(*args, **kwargs)
        args[2].bot.send_message(
            chat_id=args[1].effective_chat.id,
            text=message)
        return message
    return wrapper_send


def tag(func):
    @functools.wraps(func)
    def wrapper_tag(*args, **kw):
        tag = args[0].dao.tag_exists(args[2].args[0])
        if not tag:
            raise TelegramError("Wie heißt denn die List?")
    return wrapper_tag


def context_args(arg_count):
    def decorator(func):
        @functools.wraps(func)
        def wrapper_context_args(*args, **kwargs):
            if (len(args[2].args) < arg_count):
                raise TelegramError("Leider zu wenige Argumente")
            tag = args[2].args[0]
            command_args = args[2].args[1:]
            return func(args[0], args[1], args[2], tag, command_args)
        return wrapper_context_args
    return decorator


def telegram_command(func):
    @functools.wraps(func)
    def wrapper_telegram_command(self, *args, **kwargs):
        kwargs['update'] = args[0]
        kwargs['context'] = args[1]
        tag = None
        command_args = None
        if(len(args[1].args) > 0):
            tag = args[1].args[0]
            if(len(args[1].args) > 1):
                command_args = args[1].args[1:]
        return func(self, tag, command_args, **kwargs)
    return wrapper_telegram_command


class View(object):

    def __init__(self, dao):
        self.logger = logging.getLogger(__name__)
        self.dao = dao

    def convert_ts(self, timestamp):
        return datetime.datetime.fromtimestamp(timestamp).strftime('%d.%m.%Y')

    def print_column(self, table, column):
        result = ''
        for i, row in enumerate(table):
            result += '{}. {} \n'.format(i+1, row[column])
        return result

    @send
    @telegram_command
    def all_lists_handler(self, tag, command_args, **kw):
        all_lists = self.dao.all_lists()
        return self.print_column(all_lists, 1)

    @send
    @telegram_command
    def add_new_list_handler(self, tag, command_args, **kw):
        if not tag:
            raise TelegramError("Keine Liste:(")
        if self.dao.tag_exists(tag):
            raise TelegramError("Diese Liste gibt es schon:)")
        self.dao.new_list(tag)
        return "neue Liste '{}' erstellt".format(tag)

    @send
    @telegram_command
    def add_items_to_list_handler(self, tag, command_args, **kw):
        if not tag:
            raise TelegramError("Zu welcher Liste soll ich die Sachen"
                                "hinzufügen?")
        if not self.dao.tag_exists(tag):
            raise TelegramError("Diese Liste '{}’ finde ich nicht".format(tag))
        if not command_args:
            raise TelegramError("Was soll ich denn hinzufügen?")
        self.dao.add_items_to_list(command_args, tag)
        return self.print_column(self.dao.get_content(tag), 0)

    @send
    @telegram_command
    def get_content_handler(self, tag, command_args, **kw):
        if not tag:
            raise TelegramError("Welche Liste soll ich ausgeben?")
        if not self.dao.tag_exists(tag):
            raise TelegramError("Diese Liste '{}’ finde ich nicht".format(tag))
        items = self.dao.get_content(tag)
        return self.print_column(items, 0)

    @send
    @telegram_command
    def delete_list_handler(self, tag, command_args, **kw):
        if not tag:
            raise TelegramError("Welche Liste soll ich löschen?")
        if not self.dao.tag_exists(tag):
            raise TelegramError("Diese Liste '{}’ finde ich nicht".format(tag))
        self.dao.delete_list(tag)
        return "Liste {} gelöscht".format(tag)

    @send
    @telegram_command
    def delete_items_from_list_handler(self, tag, command_args, **kw):
        if not tag:
            raise TelegramError("Von welcher Liste soll ich löschen?")
        if not self.dao.tag_exists(tag):
            raise TelegramError("Diese Liste '{}’ finde ich nicht".format(tag))
        if not command_args:
            raise TelegramError("Jetzt habe ich ja gar nix zu löschen:)")
        save_to_delete = self.dao.items_exist(command_args, tag)
        for item in save_to_delete:
            self.dao.delete_item_from_list(item, tag)
        return "Gelöscht von {}: {}".format(tag, ' '.join(save_to_delete))

        







