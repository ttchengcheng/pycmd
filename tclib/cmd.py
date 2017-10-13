#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""cmd helper functions"""

# import this to avoid the pylint warning ("Unnecessary parens after 'print' keyword")
from __future__ import print_function
import os
import sys
import subprocess
import colorama


class Cmd(object):
    "command line util"

    @classmethod
    def color_prompt(cls):
        "color used for showing prompt message"
        return colorama.Fore.LIGHTGREEN_EX

    @classmethod
    def color_error(cls):
        "color used for showing error message"
        return colorama.Fore.LIGHTRED_EX

    @classmethod
    def color_cmd(cls):
        "color used for showing command line"
        return colorama.Fore.LIGHTYELLOW_EX

    @classmethod
    def color_data(cls):
        "color used for showing data message"
        return colorama.Fore.LIGHTCYAN_EX

    @classmethod
    def home_dir(cls):
        "absolute home dir path"
        return os.path.expanduser("~")

    def __init__(self):
        "init"
        colorama.init(autoreset=True)

    @classmethod
    def user_dir(cls, file_name):
        "get expand str ~/file_name"
        is_empty_name = len(file_name) > 0
        if (not is_empty_name) and (file_name[0] in ['\\', '/']):
            file_name = file_name[1:]

        return os.path.join(cls.home_dir(), file_name)

    @classmethod
    def show_error(cls, msg):
        "print error message"
        print(cls.color_error() + msg)

    @classmethod
    def show_cmd(cls, cmd):
        "print command"
        print(cls.color_cmd() + cmd)

    @classmethod
    def show_prompt(cls, prompt):
        "print prompt"
        return input(cls.color_prompt() + prompt)

    @classmethod
    def show_data(cls, prompt):
        "print data"
        print(cls.color_data() + str(prompt))

    @classmethod
    def show_output(cls, output):
        "print normal output"
        print(output)

    @classmethod
    def exec_cmd(cls, params, path='.'):
        "echo and exec a command line command"

        if not params:
            sys.exit(0)

        cls.show_cmd('> ' + ' '.join(params))

        try:
            cmd_output = subprocess.check_output(
                params, cwd=path).decode('utf-8')
            if cmd_output:
                print(cmd_output)
        except subprocess.CalledProcessError as exec_except:
            cls.show_error(exec_except.output.decode('utf-8'))

    @classmethod
    def exec_sys(cls, params, path='.'):
        "echo and exec a sys command"
        cls.show_cmd('> ' + ' '.join(params))

        try:
            cmd_output = subprocess.check_output(
                ' '.join(params), cwd=path, shell=True).decode('utf-8')
            if cmd_output:
                print(cmd_output)
        except subprocess.CalledProcessError as exec_except:
            cls.show_error(exec_except.output.decode('utf-8'))


INSTANCE = Cmd()
