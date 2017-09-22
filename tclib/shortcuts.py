#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""cmd shortcuts storage"""

import os
from tinydb import TinyDB, Query


class Shortcut(object):
    "class for accessing shortcut data"

    data_file = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), '../cdx/data.json')

    def __init__(self):
        self.data_base = TinyDB(self.data_file)

    def all(self):
        "read all shortcuts"
        return self.data_base.all()

    def set(self, shortcut, path):
        "insert/update shortcut"

        new_query = Query()
        query_result = self.data_base.search(new_query.shortcut == shortcut)
        if query_result:
            self.data_base.update({'path': path}, new_query.shortcut == shortcut)
        else:
            self.data_base.insert({'shortcut': shortcut, 'path': path})

    def unset(self, shortcut):
        "remove shortcut"
        new_query = Query()
        self.data_base.remove(new_query.shortcut == shortcut)

    def search(self, keyword):
        "search keyword for shortcut"
        new_query = Query()
        return self.data_base.search(new_query.shortcut == keyword)

    def fuzzy_search(self, keyword):
        "fuzzy search keyword for shortcut"
        new_query = Query()
        return self.data_base.search(new_query.shortcut.test(lambda val: keyword in val))

    @staticmethod
    def build_print_table(result):
        "print table data"

        table = [['shortcut', 'path']]
        for entries in result:
            table.append([entries['shortcut'], entries['path']])

        return table
