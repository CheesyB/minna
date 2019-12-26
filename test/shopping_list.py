#!/usr/bin/env python


class ShoppingList(object):

    """Docstring for ShoppingList. """

    def __init__(self):
       self.list = []

    def add_item(self, item):
        if item not in self.list:
            self.list.append(item)

    def pretty_print(self):
        return '\n'.join(self.list)
