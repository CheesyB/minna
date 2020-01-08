#!/usr/bin/env python


import sqlite3
import logging
import time


class SqlAdapter():

    """Docstring for SqlAdapter. """

    def __init__(self, connection):
        self.con = connection
        self.con.text_factory = lambda x: x.decode("utf-8")
        self.c = self.con.cursor()
        self.logger = logging.getLogger(__name__)
        self.init_db()

    def all_lists(self):
        return self.c.execute('''
            SELECT * FROM lists
            ''').fetchall()

    def tag_exists(self, tag):
        return self.c.execute('''
            SELECT id FROM lists
            WHERE tag = ?''', (tag,)).fetchone()

    def init_db(self):
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS lists (
            id INTEGER NOT NULL PRIMARY KEY,
            tag VARCHAR(20) NOT NULL UNIQUE,
            timestamp DATE
            ); '''
                       )
        self.logger.info("created table lists")

        self.c.execute('''
            CREATE TABLE IF NOT EXISTS items (
            id INTEGER NOT NULL PRIMARY KEY,
            item VARCHAR(30) NOT NULL UNIQUE,
            times_used INT NOT NULL
            ); '''
                       )
        self.logger.info("created table items")

        self.c.execute('''
            CREATE TABLE IF NOT EXISTS items_lists (
            item INT NOT NULL,
            list INT NOT NULL,
            UNIQUE(item, list) ON CONFLICT ABORT
            FOREIGN KEY(item) REFERENCES items(id),
            FOREIGN KEY(list) REFERENCES lists(id)
            ); '''
                       )
        self.logger.info("created table item_lists")

    def new_list(self, tag):
        self.c.execute(''' INSERT INTO lists (timestamp,tag) values(?,?)''',
                       (time.time(), tag))
        self.logger.info('new list added {}'.format(tag))

    def add_item(self, item):
        self.c.execute('''
                INSERT INTO items (item, times_used)
                VALUES(?,1)
                ON CONFLICT(item)
                DO UPDATE SET times_used = times_used + 1''', (item,))
        self.logger.info('added {} to items'.format(item))

    def map_item_to_list(self, item, tag):
        self.c.execute('''
                INSERT INTO items_lists (item, list )
                values((SELECT id FROM items WHERE item = ?),
                        (SELECT id FROM lists WHERE tag = ?))''', (item, tag))
        self.logger.info('added {} to {}'.format(item, tag))

    def delete_item_from_list(self, item, tag):
        self.c.execute('''
            DELETE FROM items_lists AS il
            WHERE  il.item = (
                SELECT id FROM items
                 WHERE items.item = ?)
            AND il.list = (
                SELECT id FROM lists
                WHERE lists.tag = ?)''', (item, tag))
        self.logger.info("deleted {} from list {}".format(item, tag))

    def delete_list(self, tag):
        self.c.execute('''
            DELETE FROM lists
            WHERE tag = ?''', (tag,))
        self.logger.info("deleted list {}".format(tag))

    def delete_mapping(self, tag):
        self.c.execute('''
            DELETE FROM items_lists AS il
            WHERE il.list = (
                SELECT id FROM lists
                WHERE tag = ?)''', (tag,))
        self.logger.info("deleted mapping {}".format(tag))

    def get_content(self, tag):
        return self.c.execute('''
            SELECT i.item FROM items as i
            INNER JOIN items_lists as il ON il.item = i.id
            INNER JOIN lists as l ON il.list = l.id
            WHERE l.tag = ? ''', (tag,)).fetchall()
