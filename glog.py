#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""show git log with gitql"""

import sys
import os
import subprocess
import tclib.cmd as tc_cmd
import tclib.shortcuts as tc_shortcut

CMD = tc_cmd.Cmd()
def glog():
    "exec git log with shortcut directory"

    exec_path = '.'

    if len(sys.argv) >= 2:
        shortcuts = tc_shortcut.Shortcut()
        search_result = shortcuts.search(sys.argv[1])

        if sys.argv[1] != '.':
            if search_result:
                exec_path = search_result[0]['path']
            else:
                CMD.show_error('shortcut [' + sys.argv[1] + "] can't be found")
                sys.exit(2)

    if exec_path == '.':
        exec_path = os.path.realpath('.')

    if not os.path.isdir(exec_path):
        CMD.show_error("[{1}]{0} is not a valid path.".format(
            exec_path, sys.argv[1]))
        sys.exit(2)

    CMD.show_cmd('(' + exec_path + ')')

    subprocess.Popen(['git', 'log', '-7'] + sys.argv[2:], cwd=exec_path)

glog()
