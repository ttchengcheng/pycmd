#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""convert csv file to xls file"""

import argparse
import os
import sys
import csv
import shlex
import codecs
import tablib
import tclib.cmd as tc_cmd


def get_full_path(arg_options):
    "check and return full path of file"

    path = os.path.realpath(arg_options.file)
    if os.path.isfile(path):
        return path

    return ""


def save_as_xls(csv_file_path, encoding='utf-8'):
    "Save csv file to xls file"

    data = []
    with codecs.open(csv_file_path, 'r', encoding) as csv_file:
        csv_reader = csv.reader(csv_file)
        # headers = next(csv_reader)
        for row in csv_reader:
            data.append(tuple(row))

    data = tablib.Dataset(*data)

    if csv_file_path.endswith('.csv'):
        xls_file_path = csv_file_path[0:-4]

    xls_file_path = xls_file_path + '.xls'

    with open(xls_file_path, 'wb') as file_xls:
        file_xls.write(data.export('xls'))

    return xls_file_path, ""


if __name__ == "__main__":
    CMD = tc_cmd.INSTANCE

    # command line arguments
    PARSER = argparse.ArgumentParser(
        description='Convert csv file to xls file',
    )
    PARSER.add_argument('file', action="store", type=str,
                        help="input file")

    PARSER.add_argument('-e', action="store", type=str,
                        dest='encoding', default='utf-8', help="file encoding")

    PARSER.add_argument('--o', action="store_true", dest="open",
                        help="open xls when converting finished")

    OPTIONS = PARSER.parse_args()
    FULL_PATH = get_full_path(OPTIONS)

    if not FULL_PATH:
        CMD.show_error("File [{0}] cannot be located.".format(OPTIONS.file))
        sys.exit(2)

    XLS_FILE_PATH, ERR_MSG = save_as_xls(FULL_PATH, OPTIONS.encoding)
    if ERR_MSG:
        CMD.show_error('Saving xls file failed: ' + ERR_MSG)
        sys.exit(2)
    else:
        CMD.show_output('File {0} is sucessfully saved'.format(XLS_FILE_PATH))

    if OPTIONS.open:
        CMD.exec_sys(['open', shlex.quote(XLS_FILE_PATH)])
