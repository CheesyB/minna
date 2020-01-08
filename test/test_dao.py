#!/usr/bin/env python

import unittest
import sqlite3
from minna.dao import Dao
from minna.sql_adapter import SqlAdapter
from telegram.error import TelegramError


class DaoTest(unittest.TestCase):

    def setUp(self):
        connection = sqlite3.connect(":memory:")
        self.adapter = SqlAdapter(connection)
        self.under_test = Dao(self.adapter)

    def test_new_list(self):
        self.under_test.new_list("test")
        self.assertEqual("test", self.adapter.all_lists()[0][1])
    
    def test_get_content_list_does_not_exist(self):
        with self.assertRaises(TelegramError):
            self.under_test.get_content("gibtsNicht")


    def test_add_items_to_list(self):
        items = ["Tomate", "Hase", "Gurke", "Martini"]
        self.under_test.new_list("test")
        self.under_test.add_items_to_list(items, "test")
        result = self.under_test.get_content("test")
        self.assertCountEqual(items, result)

    def test_delete_items_from_list(self):
        items = ["Tomate", "Hase", "Gurke", "Martini"]
        self.under_test.new_list("test")
        self.under_test.add_items_to_list(items, "test")
        self.under_test.delete_item_from_list("Tomate", "test")
        result = self.under_test.get_content("test")
        self.assertCountEqual(items[1:], result)


