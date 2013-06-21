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

import os
import pywikibot
import simplejson

wikidata = pywikibot.Site('wikidata', 'wikidata')

# This script notifies users that their job has completed.
# It should run from cron every 12 hours or so.

filename = os.path.expanduser('~/public_html/archives/all.json')


def update_notified(jobs):
    with open(filename, 'r') as f:
        data = simplejson.load(f)
    for job in jobs:
        data['jobs'][job]['notified'] = True
    with open(filename, 'w') as f:
        simplejson.dump(data, f)


with open(filename, 'r') as f:
    data = simplejson.load(f)

users = {}

for eyedee in data['jobs']:
    if data['jobs'][eyedee]['notified']:
        # Already done
        continue
    job = data['jobs'][eyedee]
    user = job['job']['user']
    if user in users:
        users[user].append(eyedee)
    else:
        users[user] = [eyedee]

for user in users:
    msg = ''
    num = len(users[user])
    for eyedee in users[user]:
        msg += '* [//tools.wmflabs.org/matilda/cgi-bin/api.py?job={0} {0}]\n'.format(eyedee)
    temp = '{{subst:User:Legobot/Message|content=%s|num=%s|sig=~~~~}}' % (msg, num)
    pg = pywikibot.Page(wikidata, user, ns=3)
    text = pg.get()
    text += '\n' + temp
    summary = 'Bot: Notifying user of {0} completed jobs'.format(num)
    pg.put(text, summary, minorEdit=False)
    # Now mark the jobs as completed
    update_notified(list(users[user]))
