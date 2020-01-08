#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.error import TelegramError

import pprint
import datetime
import logging
import re


class Dao(object):

    def __init__(self, sqlAdapter):
        self.adapter = sqlAdapter
        self.logger = logging.getLogger(__name__)

    def all_lists(self):
        return self.adapter.all_lists()

    def new_list(self, tag):
        if self.adapter.tag_exists(tag):
            raise TelegramError("Liste gibt es bereits:)")
        self.adapter.new_list(tag)

    def get_content(self, tag):
        if not self.adapter.tag_exists(tag):
            raise TelegramError("Diese Liste gibt's nicht")
        return [it[0] for it in self.adapter.get_content(tag)]
    
    def add_items_to_list(self, items, tag):
        for item in items:
            self.adapter.add_item(item)
            self.adapter.map_item_to_list(item, tag)
    
    def add_item_to_list(self, item, tag):
        self.adapter.add_item(item)
        self.adapter.map_item_to_list(item, tag)


    def delete_items_from_list(self, items, tag):
        for item in items:
            self.adapter.delete_item_from_list(item, tag)

    def delete_item_from_list(self, item, tag):
        self.adapter.delete_item_from_list(item, tag)


    def delete_list(self, tag):
        self.adapter.delete_list(tag)
