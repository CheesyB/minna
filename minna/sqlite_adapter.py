#!/usr/bin/env python


import sqlite3
import time

def initializeDB(cursor):
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS lists ( 
        id INTEGER NOT NULL PRIMARY KEY,
        tag VARCHAR(20),
        timestamp INT
        ); '''
    )
    cursor.execute( '''
        CREATE TABLE IF NOT EXISTS items (
        id INTEGER NOT NULL PRIMARY KEY,
        item VARCHAR(30)
        ); '''
    )
    cursor.execute( '''
        CREATE TABLE IF NOT EXISTS items_lists (
        item INT NOT NULL,
        list INT NOT NULL,
        FOREIGN KEY(item) REFERENCES itms(id),
        FOREIGN KEY(list) REFERENCES list(id)
        ); '''
    )

def insertStuff(cursor):
    cursor.execute(
            'INSERT INTO lists(tag, timestamp) values (?, ?)', 
            ["test", int(time.time())]
        )
    cursor.execute(
            'INSERT INTO lists(tag, timestamp) values (?, ?)', 
            ["tim", int(time.time())]
        )
    cursor.execute('INSERT INTO lists(tag, timestamp) values (?, ?)', ["anna", time.time()])
    
    mylist =  [("Tomate",), ("Banane",), ("Kaffee",), ("Grünkohl",), ("Bier",) ]

    cursor.executemany('INSERT INTO items(item) values (?)', mylist )
    cursor.executemany('INSERT INTO items_lists(item, list) values (?, ?)', [
        (1,1),(2,1),(3,1),(5,1),(1,2),(3,2),(4,2)])


def getStuff(cursor):
    print(cursor.execute('SELECT * FROM items').fetchall())
    print(cursor.execute('SELECT * FROM lists').fetchall())
    print(cursor.execute(''' 
        SELECT i.item FROM items as i
        INNER JOIN items_lists as il ON il.item = i.id
        INNER JOIN lists as l ON il.list = l.id
        WHERE l.id = 2 ''').fetchall())
    #JOIN items_lists ON items.id = items_lists.item



if __name__ == "__main__": 
    conn = sqlite3.connect(':memory:')
    c = conn.cursor()
    initializeDB(c)
    insertStuff(c)
    getStuff(c)



