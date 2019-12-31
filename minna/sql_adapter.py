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
        self.initDB()
        self.insertStuff()

    @property
    def latest_list(self):
        latest_id = self.c.execute('''
            SELECT id FROM lists
            ORDER BY id DESC
            LIMIT 1 ''').fetchone()[0]
        self.logger.info('latest list id is {}'.format(latest_id))
        return latest_id

    @property
    def allLists(self):
        return self.c.execute('''
            SELECT * FROM lists
            ''').fetchall()

    def check_raise(self, tag):
        if not (self.c.execute('''
        SELECT id FROM lists
        WHERE tag = ?''', (tag,)).fetchone()):
            raise Exception("no list with tag {}".format(tag))

    def initDB(self):
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

    def newList(self, tag):
        self.c.execute(''' INSERT INTO lists (timestamp,tag) values(?,?)''',
                       (time.time(), tag))
        self.logger.info('new list added {}'.format(tag))

    def addItemsToList(self, items, tag):
        self.check_raise(tag)

        for item in items:
            try:
                self.c.execute('''
                        INSERT INTO items (item, times_used)
                        VALUES(?,1)
                        ON CONFLICT(item)
                        DO UPDATE SET times_used = times_used + 1''', (item,))
                self._mapItemToList(item, tag)
            except Exception as e:
                self.logger.info(e)
                raise e

    def _mapItemToList(self, item, tag):
        try:
            self.c.execute('''
                    INSERT INTO items_lists (item, list )
                    values((SELECT id FROM items WHERE item = ?),
                            (SELECT id FROM lists WHERE tag = ?))''', (item, tag))
        except sqlite3.IntegrityError:
            self.logger.warning(
                "item {} already in list {}".format(item, tag))
            return
        self.logger.info('added {} to {}'.format(item, tag))

    def deleteItemFromList(self, item, tag):
        self.check_raise(tag)
        self.c.execute('''
            DELETE FROM items_lists AS il
            WHERE  il.item = (
                SELECT id FROM items
                 WHERE items.item = ?)
            AND il.list = (
                SELECT id FROM lists
                WHERE lists.tag = ?)''', (item, tag))
        self.logger.info("deleted {} from list {}".format(item,tag))

    def deleteList(self, tag):
        self.check_raise(tag)
        self.c.execute('''
            DELETE FROM items_lists AS il
            WHERE il.list = (
                SELECT id FROM lists
                WHERE tag = ?)''', (tag,))
        self.logger.info("deleted mapping {}".format(tag))
        self.c.execute('''
            DELETE FROM lists
            WHERE tag = ?''', (tag,))
        self.logger.info("deleted list {}".format(tag))



    def getContent(self, tag):
        self.check_raise(tag)
        return self.c.execute('''
            SELECT i.item FROM items as i
            INNER JOIN items_lists as il ON il.item = i.id
            INNER JOIN lists as l ON il.list = l.id
            WHERE l.tag = ? ''', (tag,)).fetchall()

    def insertStuff(self):

        self.newList("tutiuti")
        self.newList("TimTest")
        self.newList("Paris")
        self.newList("Einkauf")

        self.addItemsToList(["Nudeln", "Bohnen", "Gurken", "Tomate"], "TimTest")
        self.addItemsToList(["Nudeln", "Banane", "Gurken", "Tomate"], "Einkauf")
        self.addItemsToList(["Nudeln", "Apfel", "Gurken", "Tomate" ], "Paris")
        self.addItemsToList(["Nudeln", "Nudeln", "Gurken", "Tomate"], "tutiuti")
        self.addItemsToList(["Tomate", "Makrelen", "Tim", "Tim_Tom"], "Einkauf")

        try:
            self.addItems(["Nudeln", "Apfel", "Gurken", "Tomate"], "GibtsNicht")
        except Exception as e:
            print(e)

    def getStuff(self):
        print("Items: {}".format(self.c.execute('SELECT * FROM items').fetchall()))
        print("Lists: {}".format(self.c.execute('SELECT * FROM lists').fetchall()))
        result = self.c.execute('''
            SELECT i.item FROM items as i
            INNER JOIN items_lists as il ON il.item = i.id
            INNER JOIN lists as l ON il.list = l.id
            WHERE l.id = 4 ''').fetchall()
        return result


if __name__ == "__main__":

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.DEBUG)
    connection = sqlite3.connect(':memory:')
    sqlAdaper = SqlAdapter(connection)
    sqlAdaper.insertStuff()
    sqlAdaper.getStuff()
    sqlAdaper.deleteItemFromList("Apfel", 4)
    print("allLists: {}".format(sqlAdaper.allLists))
    print(sqlAdaper.getStuff())
