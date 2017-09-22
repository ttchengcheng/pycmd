#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""clean git settings"""

import sys
import tclib.cmd as tc_cmd

CMD = tc_cmd.Cmd()
THE_INPUT = CMD.show_prompt("Remove all git settings? (y/n)")
if THE_INPUT != 'y':
    sys.exit(1)

CMD.exec_sys([r'rm', '-rf', '.git'])
CMD.exec_sys([r'rm', '-rf', '.gitignore'])
