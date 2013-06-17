#!/usr/bin/env python
from __future__ import unicode_literals
"""
Copyright (C) 2013 Legoktm

Licensed as CC-Zero. See https://creativecommons.org/publicdomain/zero/1.0 for more details.
"""
import hashlib
import mwparserfromhell as mwparser
import os
import pywikibot
import simplejson
import traceback
import wdapi

wikidata = pywikibot.DataSite('wikidata','wikidata')

pywikibot.handleArgs()

LOG_PATH = os.path.expanduser('~/public_html/archives')
if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)
LOG_PATH += '/'


def md5(value):
    return hashlib.md5(value).hexdigest()

# SOURCE_VALUES

page = pywikibot.Page(wikidata, 'Wikidata:List of wikis/python')
SOURCE_VALUES = simplejson.loads(page.get())
SOURCE_VALUES = SOURCE_VALUES['wikipedia']
for lang in SOURCE_VALUES:
    SOURCE_VALUES[lang] = pywikibot.ItemPage(wikidata, SOURCE_VALUES[lang])

def create_all_json():
    # Creates the LOGPATH + 'all.json' file.
    filename = LOG_PATH + 'all.json'
    if os.path.exists(filename):
        # huh???
        return
    d = {'jobs': {},
         'updated': str(pywikibot.Timestamp.today()),
         }
    with open(filename, 'w') as f:
        simplejson.dump(d, f)


class Log:
    def __init__(self, job):
        self.job = job  # Job class
        self.start = pywikibot.Timestamp.today()
        self.data = list()

    def append(self, value):
        # values are dict objects
        self.data.append(value)

    def abort(self, code, msg):
        """

        @param code: machine readable error code
        @param msg: human readable explanation
        @return: nothing
        """
        # TODO: Do something else here.

        self.finish('aborted', errorcode=code, error=msg)

    def finish(self, status, **kwargs):
        d = {'start': str(self.start),
             'finish': str(pywikibot.Timestamp.today()),
             'job': self.job.toJSON(),
             'edits': self.data,
             'id': self.job.toMD5(),
             'status': status,
             'notified': False
             }
        for kw in kwargs:
            # Let us override values if we want to.
            d[kw] = kwargs[kw]
        filename = LOG_PATH + self.job.toMD5() + '.json'
        with open(filename, 'w') as f:
            simplejson.dump(d, f)
        print 'Saved to {0}.'.format(filename)
        # Now we need to update the all.json file.
        create_all_json()  # Make sure it already exists
        # Modify the current dict
        del d['edits']
        d['filename'] = filename
        with open(LOG_PATH + 'all.json', 'r') as f:
            all_data = simplejson.load(f)
        all_data['jobs'][d['id']] = d
        all_data['updated'] = str(pywikibot.Timestamp.today())
        with open(LOG_PATH + 'all.json', 'w') as f:
            simplejson.dump(all_data, f)
        # Ok we're done.


class Job:
    def __init__(self, line):
        self._start = pywikibot.Timestamp.today()
        self.repo = wikidata
        #parse the line
        temp = mwparser.parse(line).filter_templates()[0]
        data = {'lang': unicode(temp.get(1).value),
                'source': unicode(temp.get(2).value),
                'pid': unicode(temp.get(3).value),
                'target_qid': unicode(temp.get(4).value),
                'row': line,  # Do we even need this?
                'user':unicode(temp.get(5).value),
                }
        #build the summary
        #lets build some options
        whitelist = ('ignoreprefix','create','ignore','recursion','pid','qid')
        for param in temp.params:
            if unicode(param.name).startswith(whitelist):
                data[unicode(param.name)] = unicode(param.value)
        print data
        self.data = data

        #set up some easy variables to access (named in original script)
        self.lang = self.data['lang']
        self.source = self.data['source']
        self.local_site = pywikibot.Site(self.data['lang'], 'wikipedia')
        self.recursion = int(self.data.get('recursion', 0))

        self.create = not ('nocreate' in self.data)

        if 'ignoreprefix' in self.data:
            self.ignore_prefix = self.data['ignoreprefix'].split(',')
        else:
            self.ignore_prefix = list()

        if 'ignore' in self.data:
            self.ignore = self.data['ignore'].split(',')
        else:
            self.ignore = list()

    def run(self):
        # start logging
        self.log = Log(self)
        if self.source.startswith(tuple(self.local_site.namespaces()[14])):
            category = pywikibot.Category(self.local_site, self.source)
            try:
                print 'Fetching %s ' % (category.title().encode('utf-8'))
            except UnicodeDecodeError:
                pass
            gen = category.articles(namespaces=[0], recurse=self.recursion)
        elif self.source.startswith(tuple(self.local_site.namespaces()[10])):
            template = pywikibot.Page(self.local_site, self.source)
            gen = template.getReferences(follow_redirects=False, onlyTemplateInclusion=True, namespaces=[0])
        else:
            self.log.abort('badgenerator', 'A valid generator could not be parsed')
            raise ValueError("Could not parse generator.")

        #construct the claim
        self.claim = pywikibot.Claim(self.repo, self.data['pid'])
        self.claim.setTarget(pywikibot.ItemPage(self.repo, self.data['target_qid']))

        if self.lang in SOURCE_VALUES:
            self.sources = pywikibot.Claim(self.repo, 'p143')
            self.sources.setTarget(SOURCE_VALUES[self.lang])
        else:
            self.sources = None

        for page in gen:
            self.run_page(page)

    def run_page(self, page):
        page_data = {'site': page.site.dbName(),
                     'title': page.title(),
                     }
        item = pywikibot.ItemPage.fromPage(page)
        if not item.exists():
            if self.create:
                try:
                    item = wdapi.createItem(page)
                except:
                    tb = traceback.format_exc()
                    l = {'status': 'couldnotcreate',
                         'traceback': tb,
                         'page': page_data,
                         }
                    self.log.append(l)
                    return
            else:
                l = {'status': 'doesnotexist',
                     'page': page_data,
                     }
                self.log.append(l)
                return

        #set up the logger data
        l = {'item': item.getID(),
             'page': page_data}
        for prefix in self.ignore_prefix:
            if page.title().startswith(prefix):
                l['status'] = 'blacklist'
                l['blacklist'] = {'type': 'prefix', 'value': prefix}
                self.log.append(l)
                return

        if page.title() in self.ignore:
            l['status'] = 'blacklist'
            l['blacklist'] = {'type': 'exact', 'value': page.title()}
            self.log.append(l)
            return

        if page.isRedirectPage():
            l['status'] = 'redirect'
            self.log.append(l)
            return

        ok, error = wdapi.canClaimBeAdded(item, self.claim, checkDupe=True)
        if ok:
            item.addClaim(self.claim, bot=True)
            if self.sources:
                self.claim.addSource(self.sources, bot=True)
            l['status'] = 'success'
        else:
            l['status'] = 'constraint'
            l['constraint'] = error

        self.log.append(l)

    def toJSON(self):
        # Why do we need this again?
        return self.data

    def toMD5(self):
        # Unique for each job b/c of request parameters and time when instantiated.
        # As long as the same job object gets passed around, we'll be fine.
        if not hasattr(self, '_md5'):
            self._md5 = md5(simplejson.dumps(self.toJSON()) + str(self._start))
        return self._md5


class FeedBot:
    def __init__(self):
        self.site = wikidata
        self.page = pywikibot.Page(self.site, 'User:Legobot/properties.js')

    def run(self):
        jobs = self.page.get().splitlines()
        for job in jobs:
            if job.startswith('#') or not job.strip():
                continue
            self.run_job(job)
            current = self.page.get(force=True)
            current = current.replace(job + '\n', '').strip()
            self.page.put(current, 'Bot: Removing archived job')

    def run_job(self, job):
        j = Job(job)
        j.run()




if __name__ == "__main__":
    robot = FeedBot()
    robot.run()
