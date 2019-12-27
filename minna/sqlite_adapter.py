#!/usr/bin/env python


import sqlite3
import logging
import time


class SqlAdapter():

    """Docstring for SqlAdapter. """

    def __init__(self, connection):
        self.conn = connection
        self.c = self.conn.cursor()
        self.logger = logging.getLogger(__name__)
        self.initDB()

    @property
    def latest_list(self):
        latest_id = self.c.execute(''' 
            SELECT id FROM lists
            ORDER BY id DESC
            LIMIT 1 ''').fetchone()[0]
        self.logger.info('current list id is {}'.format(latest_id))
        return latest_id

    def initDB(self):
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS lists (
            id INTEGER NOT NULL PRIMARY KEY,
            tag VARCHAR(20) UNIQUE,
            timestamp INT
            ); '''
                       )
        self.logger.info("created table lists")

        self.c.execute('''
            CREATE TABLE IF NOT EXISTS items (
            id INTEGER NOT NULL PRIMARY KEY,
            item VARCHAR(30) NOT NULL UNIQUE
            ); '''
                       )
        self.logger.info("created table items")

        self.c.execute('''
            CREATE TABLE IF NOT EXISTS items_lists (
            item INT NOT NULL,
            list INT NOT NULL,
            FOREIGN KEY(item) REFERENCES itms(id),
            FOREIGN KEY(list) REFERENCES list(id)
            ); '''
                       )
        self.logger.info("created table item_lists")

    def newList(self, tag=None):
        self.c.execute(''' INSERT INTO lists (timestamp,tag) values(?,?)''',
                (time.time(), tag))
        self.logger.info('new list added')

    def addItems(self, items, tag=None):
        for item in items:
            try:
                self.c.execute('INSERT INTO items(item) values(?)', (item,))
                self.logger.info('added {} to items'.format(item))
            except Exception as e:
                self.logger.info(
                    '{} \nitem: {} already exists'.format(e, item))
        
        try:
            item_keys = self.c.execute(
                '''SELECT id FROM items WHERE item IN ({})'''.format(', '.join('?' * len(items))), items).fetchall()
            self.logger.info(
                'primary keys {}'.format(item_keys))
        except Exception as e:
            self.logger.info(e)
        
        try:
            self.c.executemany('''INSERT INTO items_lists (item, list )
                    values(?,?)''',
                    [(ik[0], self.latest_list) for ik in item_keys]
            )
        except Exception as e:
            self.logger.info(e)
        



    def insertStuff(self):
        self.c.execute(
            'INSERT INTO lists(tag, timestamp) values (?, ?)', [
                "test", int(time.time())]
        )
        self.c.execute(
            'INSERT INTO lists(tag, timestamp) values (?, ?)',
            ["tim", int(time.time())]
        )
        self.c.execute('INSERT INTO lists(tag, timestamp) values (?, ?)', [
                       "anna", time.time()])

        mylist=[("Tomate",), ("Banane",), ("Kaffee",),
                  ("Grünkohl",), ("Bier",)]

        self.c.executemany('INSERT INTO items(item) values (?)', mylist)
        self.c.executemany('INSERT INTO items_lists(item, list) values (?, ?)', [
            (1, 1), (2, 1), (3, 1), (5, 1), (1, 2), (3, 2), (4, 2)])

        self.newList("tutiuti")

    def getStuff(self):
        print(self.c.execute('SELECT * FROM items').fetchall())
        print("Lists: {}".format(self.c.execute('SELECT * FROM lists').fetchall()))
        print(self.c.execute('''
            SELECT i.item FROM items as i
            INNER JOIN items_lists as il ON il.item = i.id
            INNER JOIN lists as l ON il.list = l.id
            WHERE l.id = 4 ''').fetchall())


if __name__ == "__main__":

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.DEBUG)
    connection = sqlite3.connect(':memory:')
    sqlAdaper = SqlAdapter(connection)
    sqlAdaper.insertStuff()
    sqlAdaper.addItems(["Tomate", "Makrelen", "Tim", "Tim_Tom"])
    sqlAdaper.getStuff()



