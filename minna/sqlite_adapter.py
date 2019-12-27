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

    def getListPk(self, tag=None):
        if tag:
            list_pk = self.c.execute(' SELECT id FROM lists WHERE tag = ?',
                    (tag,)).fetchone()
            if not list_pk:
                self.logger.error("tag {} does not exist".format(tag))
                raise Exception("tag {} does not exist".format(tag))

            self.logger.info("list_pk is {}".format(list_pk))
            return list_pk
        else:
            return self.latest_list


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
            item VARCHAR(30) NOT NULL UNIQUE,
            times_used INT NOT NULL
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
        self.logger.info('new list added {}'.format(tag))

    def addItems(self, items, list_pk):
        if( list_pk > self.latest_list or list_pk < 1 ):
            raise Exception("list_pk {} out of range".format(list_pk))
        
        for item in items:
            try:
                self.c.execute(
                    ''' INSERT INTO items (item, times_used)
                        VALUES(?,1)
                        ON CONFLICT(item)
                        DO UPDATE SET times_used = times_used + 1''', (item,))
                self._mapItemToList(item, list_pk)
            except Exception as e:
                self.logger.info(e)
                raise e

    def _mapItemToList(self, item, list_pk):
        item_pk = self.c.execute(
            '''SELECT id FROM items WHERE item = ? ''', (item,)).fetchone()[0]
        self.c.execute('''INSERT INTO items_lists (item, list )
                values(?,?)''', (item_pk, list_pk))
        self.logger.info('added {} to {}'.format(
            item, list_pk))


    def insertStuff(self):



        self.newList("tutiuti")
        self.newList("TimTest")
        self.newList("Paris")
        self.newList("Einkauf")
        
        self.addItems(["Nudeln", "Bohnen", "Gurken", "Tomate"], 2)
        self.addItems(["Nudeln", "Banane", "Gurken", "Tomate"], 1)
        self.addItems(["Nudeln", "Apfel", "Gurken", "Tomate"], 4)
        try:
            self.addItems(["Nudeln", "Apfel", "Gurken", "Tomate"], 0)
        except Exception as e:
            print(e)
        

    def getStuff(self):
        print("Items: {}".format(self.c.execute('SELECT * FROM items').fetchall()))
        print("Lists: {}".format(self.c.execute('SELECT * FROM lists').fetchall()))
        print(self.c.execute('''
            SELECT i.item FROM items as i
            INNER JOIN items_lists as il ON il.item = i.id
            INNER JOIN lists as l ON il.list = l.id
            WHERE l.id = 4 ''').fetchall())


if __name__ == "__main__":

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.DEBUG)
    connection=sqlite3.connect(':memory:')
    sqlAdaper=SqlAdapter(connection)
    sqlAdaper.insertStuff()
    sqlAdaper.addItems(["Tomate", "Makrelen", "Tim", "Tim_Tom"],3)
    sqlAdaper.getStuff()
