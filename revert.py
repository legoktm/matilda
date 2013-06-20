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
import datetime
import sys
import time
import pywikibot
from pywikibot.data import api


remove = '--remove' in sys.argv
repo = pywikibot.Site('en', 'wikipedia').data_repository()
yesterday = pywikibot.Timestamp.utcnow() - datetime.timedelta(days=1)
gen = api.ListGenerator('usercontribs', site=repo, ucuser='Legobot', ucnamespace=0, ucprop='title|comment',
                        ucend=yesterday)
good = pywikibot.ItemPage(repo, 'Q174526')
bad = pywikibot.ItemPage(repo, 'Q174526')
#gen = bad.getReferences(namespaces=[0])
property = ['p135']

for page in gen:
    if not 'wbcreateclaim-create' in page['comment']:
        continue
    if not 'Q174526' in page['comment']:
        continue
    i = pywikibot.ItemPage(repo, page['title'])
    print i
    i.get()
    for prop in property:
        if prop in i.claims:
            for c in i.claims[prop]:
                if c.getTarget().getID() == bad.getID():
                    if remove:
                        print 'removing...'
                        i.removeClaims([c], bot=True)
                    else:
                        print 'changing target...'
                        c.changeTarget(good, bot=True)
                    #time.sleep(2)
