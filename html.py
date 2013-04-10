#!/usr/bin/env python
from __future__ import unicode_literals
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

def a(link, text, **attrs):
    #format the attributes
    attr = ""
    for key in attrs:
        attr += ' {}="{}"'.format(key, attrs[key])
    return '<a href="{}" {}>{}</a>'.format(link, attr, text)

form = """
      <form class="form-signin" action="/~legoktm/cgi-bin/wikidata/copypaste.py" method="get">
        <h2 class="form-signin-heading">Please enter an id.</h2>
        <input type="text" class="input-block-level" name="id" placeholder="Q##">
        <!--<input type="text" class="input-block-level" name="site" placeholder="en">-->
        <button class="btn btn-large btn-primary" type="submit">Check</button>
      </form>
"""


def form(target, method='GET', **kwargs):
    #Each kwarg should be the valuekey = {'help':'help text in front of form', 'filler':'text inside the form'}
    #These should be already translated
    text = '<form class="form-horizontal" action="{}" method="{}">'.format(target, method)
    for arg in kwargs:
        text += """<div class="control-group">
<label class="control-label" for="{0}">{1}</label>
<div class="controls">
<input type="text" id="{0}" placeholder="{2}">
</div>
</div>""".format(arg, kwargs[arg]['help'], kwargs[arg]['filler'])
    #add the submit button and close the form
    text += """ <div class="control-group">
<div class="controls">
<button type="submit" class="btn">{}</button>
</div>
</div>
</form>""".format(i18n.translate('submit'))
    return text