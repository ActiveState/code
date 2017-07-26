import sys, os
import codecs
import time
import datetime
import re
from urllib import urlopen

import yaml
from BeautifulSoup import BeautifulSoup

DELAY = 2 

RE_USER = re.compile(r'''(?x)   # verbose mode
    @                     # start of twitter user link
    <a[ ][^>]*href="/     # 'a' opening tag to the start of href url
    ([^"]*)"              # capture the user part of url to \1
    [^<]*                 # any number of non-closing bracket chars to get to:
    </a>                  # the 'a' closing tag''')
    # matches @<a href="/scarpent">scarpent</a>

RE_LINK = re.compile(r'''(?x)   # verbose mode
    <a[ ][^>]*href="      # 'a' opening tag to the start of href url
    ([^"]*)"              # capture entire url to \1
    [^>]*                 # any number of non-closing bracket chars to get to:
    >
    ([^<]*)               # any number of non-closing bracket chars to get to:
    </a>                  # the 'a' closing tag''')
    # matches <a href="http://bit.ly/Xxlch" rel="nofollow"
    #                            target="_blank">http://bit.ly/Xxlch</a>

# captures - search for twitter tags link
RE_LINK_HASH = re.compile(r'''(?x)   # verbose mode
    \[
    \/search\?q\=\%23[^\]]*
    \]
    ''')

# capture numeric status id from "published timestamp" span
RE_STATUS_ID = re.compile(r'.*/status/([0-9]*).*')
    # e.g. http://twitter.com/scarpent/status/1329714004

# ---------------

def escape(content):
    return content.replace('"', r'\"')

def print_usage(s=""):
    if s:
        print s
    print """Usage: %s twitter-account filename
    Incremental backup of twitter statuses in yaml format.
    """ % (sys.argv[0],)

# ---------------

def main(args):
    if len(args)!=2:
        return print_usage()

    username, fname  = args

    num_tweets = num_tweets_new = 0
    output = []
    output_orig = []
    by_status_id = {}

    if os.path.exists(fname):
        output_orig = [l.rstrip() for l in codecs.open(fname, "r", "utf-8").readlines()]
        content_before = yaml.load("\n".join(output_orig))
        if content_before:
            by_status_id = dict([(e["status_id"], e) 
                                 for e in content_before if "status_id" in e])

    RE_STATUS_CLASS = re.compile(r'.*\bstatus\b.*')
    url_base = "http://twitter.com/%s" % (username,)

    # let's fetch some tweets ...
    print 'Reading %s, backup in %s, started at %s' % (
           url_base, fname, datetime.datetime.today(),)
    page_nr = 0
    while True:
        page_nr += 1
        print "%3d. page - read and parse" % (page_nr,)

        num_tweets_this_page = 0

        url = '%s?page=%s' % (url_base, page_nr)
        f = urlopen(url)
        # f = open('twitter-feed.htm', 'rb')
        soup = BeautifulSoup(f.read())
        f.close()
        tweets = soup.findAll('li', {'class': RE_STATUS_CLASS})
        if len(tweets) == 0:
            break

        for tweet in tweets:
            num_tweets += 1
            current = []

            content = unicode(tweet.find('span', 'entry-content').renderContents(), 'utf8')

            content = RE_USER.sub(r'@\1', content)
            content = RE_LINK.sub(r'\2 [\1]', content)
            content = RE_LINK_HASH.sub(r'', content)

            current.append('- content : "%s"' % (escape(content),))

            date_time = tweet.find('span', 'timestamp').get("data", None)
            if date_time:
                # {date_time: time:'Sun Sep 04 20:05:28 +0000 2011'}
                # -> Sun Sep 04 20:05:28 +0000 2011
                date_time = date_time.replace("{", "").replace("}", "").replace("time:", "").strip().strip("'").strip()
                current.append('  date_time: "%s"' % (escape(date_time),))

            status_id = None
            m = RE_STATUS_ID.search(tweet.find('a', 'entry-date')['href'])
            if m:
                status_id = m.groups()[0]
                current.append('  status_id: "%s"' % (escape(status_id),))
                current.append('  url: "http://twitter.com/#!/%s/status/%s"' % (username, escape(status_id)))
            current.append("")

            if status_id is not None and status_id in by_status_id:
                # skip it
                continue

            num_tweets_new += 1
            num_tweets_this_page += 1
            output.extend(current)

        if num_tweets_this_page==0:
            print 'No new tweets found, quit iteration ...'
            break

        print '     %3d/%3d tweets saved/processed. Waiting %d seconds before fetching next page...' % (
              num_tweets_new, num_tweets, DELAY)

        # be nice to twitter's servers
        time.sleep(DELAY)

    if num_tweets_new==0:
        print 'No new tweets found in %d tweets analysed, file %s left untouched' % (num_tweets, fname)
        return False

    fout = codecs.open(fname, "w", "utf-8")
    output.extend(output_orig)
    fout.write("\n".join(output))
    print '%d/%d tweets saved in %s' % (num_tweets_new, num_tweets, fout.name)

if __name__=="__main__":
    main(sys.argv[1:])
