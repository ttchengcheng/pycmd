#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Init a git directory."""

import subprocess
import sys
import os
import tclib.cmd as tc_cmd

CMD = tc_cmd.Cmd()

# ignore file templates
IGNORE_TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'git_templates/')
IGNORE_TEMPLATES = {
    'qt': 'Qt',
    'vsc': 'VisualStudioCode',
    'py': 'Python',
    'objc': 'Objective-C',
    'go': 'Go',
    'node': 'Node'
}

# 0. check if git alreadly initialized
GIT_DIR = os.path.join(os.getcwd(), '.git')
GIT_IGNORE = os.path.join(os.getcwd(), '.gitignore')
if os.path.exists(GIT_DIR) or os.path.exists(GIT_IGNORE):
    INPUT = CMD.show_prompt('git files exist, continue? (y/n)')
    if INPUT != 'y':
        sys.exit(1)
    else:
        if subprocess.call(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gclean.py')):
            sys.exit(1)

# 1. > git init
CMD.exec_cmd(['/usr/bin/git', 'init'])

# 2. > cp {selected template} .gitignore


def get_template_path():
    "calculate template path"

    vsc_template = None
    template = sys.argv[1]
    if template.endswith('+'):
        template = template[0:-1]
        if 'vsc' in IGNORE_TEMPLATES:
            vsc_template = os.path.join(IGNORE_TEMPLATES_DIR, IGNORE_TEMPLATES['vsc'])
            vsc_template = vsc_template + '.gitignore'

    if not template in IGNORE_TEMPLATES:
        CMD.show_error("Template[{0}] cannot be found.".format(template))
        return None, None

    template = os.path.join(IGNORE_TEMPLATES_DIR, IGNORE_TEMPLATES[template])
    template = template + '.gitignore'

    print(template)
    return template, vsc_template


if len(sys.argv) > 1:
    TEMPLATE_PATH, VSC_PATH = get_template_path()
    if TEMPLATE_PATH:
        CMD.exec_cmd(['cp', TEMPLATE_PATH, '.gitignore'])
        if VSC_PATH:
            CMD.exec_sys(['cat', VSC_PATH, '>>', '.gitignore'])

# 3. > vi .gitignore
subprocess.call(os.environ.get('EDITOR', 'vi') + ' .gitignore', shell=True)

# 4. > git add .
CMD.exec_sys(['git', 'add', '.'])

# 5. > git commit -m "init"
CMD.exec_sys(['git', 'commit', '-m', '"init"'])
