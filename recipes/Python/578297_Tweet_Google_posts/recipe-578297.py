import urllib
import json
import twitter
import sqlite3
import os
from HTMLParser import HTMLParser
import nltk

class Worker(object):

    def __init__(self, profile_id, oauth, cursor):
        self.google_api_key = '---' # Google API Key
        self.profile_id = profile_id
        self.cursor  = cursor
        self.oauth = oauth

    def _get_from_gplus(self):
        if not self.profile_id: return
        data = urllib.urlopen(
            'https://www.googleapis.com/plus/v1/people/{0}/activities/public?key={1}'.format(
                self.profile_id, self.google_api_key
            )
        ).read()
        items = json.loads(data).get('items')
        if not items: return 'exists'
        the_thing = items[0]
        try:
            self.cursor.execute("insert into posts values(?)", (the_thing['url'],))
        except sqlite3.IntegrityError:
            return 'exists'
        return HTMLParser().unescape(u'G+: '+nltk.clean_html(the_thing['object']['content'])[:64]).replace('\n', ' ')+u' ... '+the_thing['url']

    def _post_to_twitter(self, tweet, user):
        if tweet == 'exists': return
        twitter.Api(**self.oauth).PostUpdate(tweet)

    def work(self):
        self._post_to_twitter(self._get_from_gplus(), 'tim')


if __name__ == "__main__":

    with sqlite3.connect(os.path.join(os.path.dirname(__file__), 'gplustotwitter.db')) as conn:
        cursor = conn.cursor()

        # Users -> Twitter OAuth credentials
        users = {'tim':{'oauth':{'consumer_key':'---',
                                'consumer_secret':'---',
                                'access_token_key':'---',
                                'access_token_secret':'---'},
                        'gplus_id':'---' #Google+ account ID
                        },
                }

        for user in users.keys():
            Worker(users[user]['gplus_id'], users[user]['oauth'], cursor).work()
        conn.commit()
