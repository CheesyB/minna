#!/usr/bin/env python

import unittest
import sqlite3
from minna.sql_adapter import SqlAdapter


class SqlAdapterTest(unittest.TestCase):

    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        self.under_test = SqlAdapter(self.connection)

    def test_add_list(self):
        self.under_test.new_list("tutiuti")
        self.under_test.new_list("TimTest")
        self.under_test.new_list("Paris")
        self.under_test.new_list("Einkauf")

    def test_insert_and_get(self):
        self.under_test.new_list("Test1")
        items = ["Nudeln", "Bohnen", "Gurken", "Tomate"]
        [self.under_test.add_item(item) for item in items]
        [self.under_test.map_item_to_list(item, "Test1") for item in items]
        retreived_items = [it[0] for it in
                           self.under_test.get_content("Test1")]
        self.assertCountEqual(items, retreived_items)

    def test_delete_items_from_list(self):
        self.under_test.new_list("test")
        items = ["Nudeln", "Bohnen", "Gurken", "Tomaten"]
        [self.under_test.add_item(item) for item in items]
        [self.under_test.map_item_to_list(item, "test") for item in items]
        self.under_test.delete_item_from_list("Tomaten", "test")
        retreived_items = [it[0] for it in
                           self.under_test.get_content("test")]
        self.assertNotIn("Tomaten", retreived_items)

    def test_delete_list(self):
        self.under_test.new_list("test")
        self.under_test.new_list("test2")
        items = ["Nudeln", "Bohnen", "Gurken", "Tomaten"]
        [self.under_test.add_item(item) for item in items]
        [self.under_test.map_item_to_list(item, "test") for item in items]
        self.under_test.delete_list("test")
        striped_lists = [li[1] for li in self.under_test.all_lists()]
        self.assertNotIn("test", striped_lists)

    def test_delete_mapping(self):
        self.under_test.new_list("test")
        self.under_test.new_list("test2")
        items = ["Nudeln", "Bohnen", "Gurken", "Tomaten"]
        [self.under_test.add_item(item) for item in items]
        [self.under_test.map_item_to_list(item, "test") for item in items]
        [self.under_test.map_item_to_list(item, "test2") for item in items]
        self.under_test.delete_mapping("test")
        self.assertEqual([], self.under_test.get_content("test"))










