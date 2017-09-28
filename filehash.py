#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""create file hash"""

import argparse
import hashlib
import math
import os
import sys
import progressbar
from tclib import cmd

CMD = cmd.INSTANCE
SUPPORTED_TYPES = ['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512']


def parse_args():
    "command line arguments"
    parser = argparse.ArgumentParser(
        description='create file hash',
    )
    parser.add_argument('file', action="store", type=str,
                        help="input file")

    parser.add_argument('-t', action="store", type=str,
                        dest='type', default='md5', choices=SUPPORTED_TYPES, help="hash type")

    parser.add_argument('--noprogress', action="store_true",
                        dest='no_progress', help="hide progressbar")

    options = parser.parse_args()

    return options


def create_hash(target_file, hash_type, no_progress):
    "create hash with file and type"

    target_file = os.path.realpath(target_file)
    if not os.path.isfile(target_file):
        CMD.show_error("{0} is not a valid file".format(target_file))
        sys.exit(2)

    hash_func = getattr(hashlib, hash_type)
    hash_value = hash_func()

    buff_size = 65536

    file_size = os.path.getsize(target_file)
    loop_count = math.ceil(file_size / buff_size)

    with open(target_file, 'rb') as file_to_hash:
        if (not no_progress) and loop_count > 64:
            progress_bar = progressbar.ProgressBar()

            for _ in progress_bar(range(loop_count)):
                data = file_to_hash.read(buff_size)
                hash_value.update(data)
        else:
            data = file_to_hash.read()
            hash_value.update(data)

    hash_value = hash_value.hexdigest()
    return hash_value


if __name__ == "__main__":
    OPTIONS = parse_args()
    print(create_hash(OPTIONS.file, OPTIONS.type, OPTIONS.no_progress))
