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
import main
data = {'en': {'basegen': 'Base generator',
               'catgen': 'Category generator',
               'tempgen': 'Pages transcluding a template',
               'wlhgen': 'Special:Whatlinkshere',
               'submit': 'Submit',
               'navbar-help': 'Help',
               'navbar-currun': 'Currently running',
               'navbar-newjobs': 'New jobs',
               },
        'qqq': {'basegen': 'The default description for a base generator',
                'catgen': 'Description for a generator that uses a category',
                'tempgen': 'Description for a generator that checks which pages transclude a template',
                'wlhgen': 'A generator that uses pagelinks, similar to [[Special:Whatlinkshere]]',
                'submit': 'Word used when submitting any form',
                'navbar-help': 'A link to the help/documentation',
                'navbar-currun': 'A link to currently running jobs',
                'navbar-newjobs': 'A link to recently submitted jobs',
                },
        }

fallbacks = {'en-gb': ['en'],
             }


def can_fallback(key, lang):
    if not lang in fallbacks:
        return False
    for l in fallbacks[lang]:
        tl = translate(key, l)
        if tl != translate(key, 'en'):
            return tl
    return False


def getlang():
    if 'uselang' in main.form:
        return main.form['uselang'].value
    return 'en'


def translate(key, lang=None):
    if not lang:
        lang = getlang()
    if lang in data:
        if key in data[lang]:
            return data[lang][key]
    fb = can_fallback(key, lang)
    if fb:
        return fb
    return data['en'][key]


