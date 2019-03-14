# -*- coding: utf-8 -*-

import sys
from textwrap import wrap

from terminaltables import SingleTable, AsciiTable


def wrap_long_text_to_table(table, text):
    max_width = table.column_max_width(0)
    return '\n'.join(wrap(text, max_width))


def get_table(table_data, title=None, ascii=False):
    if ascii or sys.platform.startswith('win'):
        return AsciiTable(table_data, title)
    else:
        return SingleTable(table_data, title)

if __name__ == '__main__':
    table_data = [
        ['test', ''],
    ]
    t = get_table(table_data, title=' execute command ')
    wrapped_string = wrap_long_text_to_table(t, "test")
    t.table_data[0][0] = wrapped_string
    print t.table