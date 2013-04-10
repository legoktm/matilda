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
import i18n
#import pywikibot


class BaseGenerator:
    def __init__(self):
        pass

    def description(self):
        if not hasattr(self, 'descrip'):
            self.descrip = i18n.translate('basegen')
        return self.descrip

    def schema(self):
        return {}


class CategoryGenerator(BaseGenerator):
    def __init__(self):
        BaseGenerator.__init__()
        pass

    def description(self):
        return i18n.translate('catgen')

    def schema(self):
        return {'site': 'pywikibot.Site',
                'cat': 'pywikibot.Page',
                'recurse': 'int',
                'namespace': 'int',
                'ignore': 'csv',
                'ignoreprefix': 'csv',
                }
