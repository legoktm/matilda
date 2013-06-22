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


import unittest

import datetime
import os
import simplejson
from matilda import matilda


class TestBot(unittest.TestCase):

    def setUp(self):
        self.line = "{{User:Legobot/properties.js/row|fr|Category:Monument historique inscrit|P107|Q618123|pid2=P31|qid2=Q10387575|pid3=P17|qid3=Q142|Ayack|nocreate=yes|recursion=2}}"

    def test_dir_creation(self):
        matilda.create_archive_dir()
        self.assertTrue(os.path.exists(os.path.expanduser('~/public_html/archives')))

    def test_all_json_creation(self):
        matilda.create_archive_dir()
        matilda.create_all_json()
        filename = os.path.expanduser('~/public_html/archives/all.json')
        self.assertTrue(os.path.exists(filename))
        with open(filename) as f:
            data = simplejson.load(f)
        self.assertTrue('updated' in data)
        self.assertTrue('jobs' in data)

    def testJob(self):
        j = matilda.Job(self.line)
        self.assertEqual(j.lang, 'fr')
        self.assertEqual(j.data['claims'], [(u'P107', u'Q618123'), (u'P31', u'Q10387575'), (u'P17', u'Q142')])
        self.assertEqual(j.source, 'Category:Monument historique inscrit')
        self.assertFalse(j.create)
        self.assertEqual(j.data['user'], 'Ayack')
        self.assertLess(j._start, datetime.datetime.today())

    def testLog(self):
        j = matilda.Job(self.line)
        l = matilda.Log(j)
        self.assertLess(l.start, datetime.datetime.today())
        self.assertEqual(l.data, [])
        l.append('test')
        self.assertEqual(l.data, ['test'])



if __name__ == "__main__":
    unittest.main()
