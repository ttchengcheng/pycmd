#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""handle fast dir navigating"""

import os
import sys
import shlex
import tclib.cmd as tc_cmd
import tclib.shortcuts as tc_shortcut
from tabulate import tabulate

CMD = tc_cmd.INSTANCE


def print_table(table):
    "print table data"
    CMD.show_data(tabulate(table, headers="firstrow", tablefmt="grid"))


def cdx_add():
    "add a cdx entry"
    argv_count = len(sys.argv)
    if argv_count < 3:
        sys.exit(0)
    dir_shortcut = sys.argv[2]

    if argv_count < 4:
        dir_to_add = os.getcwd()
    else:
        dir_to_add = sys.argv[3]

    shortcut = tc_shortcut.Shortcut()
    search_result = shortcut.search(dir_shortcut)
    if search_result:
        print_table(shortcut.build_print_table(search_result))
        if CMD.show_prompt('\nData already exist as above, replace?(y/n)') != 'y':
            sys.exit(1)

    shortcut.set(dir_shortcut, dir_to_add)
    CMD.show_output('1 entry added:')
    table = shortcut.build_print_table(shortcut.search(dir_shortcut))
    print_table(table)


def cdx_remove():
    "remove a cdx entry"
    if len(sys.argv) < 3:
        sys.exit(0)
    entry_to_remove = sys.argv[2]

    shortcut = tc_shortcut.Shortcut()
    search_result = shortcut.search(entry_to_remove)
    if search_result:
        print_table(shortcut.build_print_table(search_result))
        if CMD.show_prompt('\nThe record above will be removed, continue?(y/n)') != 'y':
            sys.exit(1)
    else:
        CMD.show_output('0 entry removed')
        sys.exit(0)

    shortcut.unset(entry_to_remove)
    CMD.show_output('1 entry removed.')


def cdx_list():
    "list all entries"

    shortcut = tc_shortcut.Shortcut()
    shortcut_data = shortcut.all()

    CMD.show_output(
        ' '.join(['Totally', str(len(shortcut_data)), 'entries.']))
    table = shortcut.build_print_table(shortcut_data)
    print_table(table)


def cdx_nav():
    """navigate to a cdx entry

        python can't change cwd of parent process,
        so this can be done with a shell function like this: (defined in sth like .bash_profile)

        _cd() {
            /Users/my/cmds/cdx.py -f cd $1
            cd `/Users/my/cmds/cdx.py $1`
        }

        _x() {
            /Users/my/cmds/cdx.py -f $1 $2
            $1 `/Users/my/cmds/cdx.py $2`
        }
    """
    if len(sys.argv) < 2:
        sys.exit(0)

    entry_to_go = sys.argv[1]
    shortcuts = tc_shortcut.Shortcut()
    search_result = shortcuts.search(entry_to_go)

    if search_result:
        entry_to_go = search_result[0]['path']

    try:
        sys.stdout.write(shlex.quote(entry_to_go))
    except IOError:
        print("{0}Command does not support pipe, {1}use cmd `cdx shortcut` {0}instead".format(
            CMD.color_error(), CMD.color_cmd()))
        sys.exit(1)


def cdx_show_cmd():
    "print a fake cdx command"
    if len(sys.argv) < 4:
        sys.exit(0)

    entry_to_go = sys.argv[3]
    operation = sys.argv[2]

    shortcuts = tc_shortcut.Shortcut()
    search_result = shortcuts.search(entry_to_go)

    if search_result:
        entry_to_go = search_result[0]['path']

    CMD.show_cmd(' '.join([operation, entry_to_go]))


def cdx_find():
    "fuzzy find enties"
    if len(sys.argv) < 3:
        sys.exit(0)

    entry_to_go = sys.argv[2]

    shortcuts = tc_shortcut.Shortcut()
    search_result = shortcuts.fuzzy_search(entry_to_go)
    table = shortcuts.build_print_table(search_result)
    print_table(table)


def cmd_route():
    "route cmd by args"
    if len(sys.argv) < 2:
        sys.exit(0)

    cdx_cmd = sys.argv[1]

    if cdx_cmd in ['a', '-a', 'add', 'append', '-add', '-append']:
        cdx_add()
    elif cdx_cmd in ['d', 'r', '-d', '-r', 'remove', 'delete', '-remove', '-delete']:
        cdx_remove()
    elif cdx_cmd in ['l', '-l', 'list', '-list']:
        cdx_list()
    elif cdx_cmd in ['-sc']:
        cdx_show_cmd()
    elif cdx_cmd in ['f', '-f', 'find', '-find', 'search', '-search']:
        cdx_find()
    else:
        cdx_nav()


cmd_route()
