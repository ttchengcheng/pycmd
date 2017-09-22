#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""show git log with gitql"""

import sys
import os
import tclib.cmd as tc_cmd
import tclib.shortcuts as tc_shortcut

EXEC_PATH = '.'
CMD = tc_cmd.Cmd()

if len(sys.argv) >= 2:
    SHORTCUTS = tc_shortcut.Shortcut()
    SEARCH_RESULT = SHORTCUTS.search(sys.argv[1])
    if SEARCH_RESULT:
        EXEC_PATH = SEARCH_RESULT[0]['path']
    else:
        CMD.show_error('shortcut [' + sys.argv[1] + "] can't be found")
        sys.exit(2)

if EXEC_PATH == '.':
    EXEC_PATH = os.path.realpath('.')

if not os.path.isdir(EXEC_PATH):
    CMD.show_error("[{1}]{0} is not a valid path.".format(EXEC_PATH, sys.argv[1]))
    sys.exit(2)

CMD.show_cmd('(' + EXEC_PATH + ')')

CMD_LINE = CMD.user_dir(
    'Documents/workspace/go/src/github.com/cloudson/gitql/gitql')
CMD_ARG = 'select date, message from commits'

CMD.exec_cmd([CMD_LINE, CMD_ARG], path=EXEC_PATH, short=True)
