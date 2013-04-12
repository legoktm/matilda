#!/usr/bin/env python
"""
Copyright (C) 2013 Legoktm

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
"""
import re
import requests
import oursql
import os
import subprocess
import sys


class SGE:
    def __init__(self, script):
        self.script = script
        self.args = list()

    def __repr__(self):
        return 'SGE(\'{}\')'.format(self.cmd)

    def __str__(self):
        return self.cmd

    def add_arg(self, value):
        if not value in self.args:
            self.args.append(value)

    def rm_arg(self, value):
        if value in self.args:
            self.args.remove(value)

    @property
    def name(self):
        if not hasattr(self, '_name'):
            self._name = self.script
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @name.deleter
    def name(self):
        self._name = self.script

    @property
    def cmd(self):
        cmd = ['qsub',
               '-N',
               self.name,
               self.script,
               ] + self.args
        return ' '.join(cmd)

    def submit(self):
        try:
            x = subprocess.check_output(self.cmd, stderr=subprocess.STDOUT, shell=True)
        except subprocess.CalledProcessError:
            return 0
        job_id = re.search('job (\d*?) \(', x).group(1)
        return int(job_id)



class DB:
    """
    Because I'm just really lazy
    """
    def __init__(self, raise_on_warnings=False):
        self.raise_on_warnings = raise_on_warnings
        self.db = None

    def open(self, force=False):
        if force or not self.is_open():
            self.db = oursql.connect(raise_on_warnings=self.raise_on_warnings,
                                     read_default_file=os.path.expanduser("~/.my.cnf"),
                                     )
        return self.db

    def cursor(self):
        return self.db.cursor(oursql.DictCursor)

    def close(self):
        self.db.close()
        self.db = None

    def is_open(self):
        return bool(self.db)


def TUSC(username, password, lang, project):
    headers = {'User-agent': 'http://tools.wmflabs.org/matilda/ by User:Legoktm'}
    # http://tools.wikimedia.de/~magnus/tusc.php?check=1&botmode=1&user=USERNAME&language=LANGUAGE&project=PROJECT&password=TUSC_PASSWORD
    params = {'check': 1,
              'botmode': 1,
              'user': username,
              'language': lang,
              'project': project,
              'password': password,
              }
    url = 'http://toolserver.org/~magnus/tusc.php'
    r = requests.post(url, params, headers=headers)
    try:
        if int(r.text) == 1:
            return True
    except Exception:
        pass
    return False
