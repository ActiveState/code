"""
   Copyright 2011 Shao-Chuan Wang <shaochuan.wang AT gmail.com>

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
"""


from AddressBook import *
from Foundation import *
import objc
import fbconsole
import urllib
import glob
import os

fbconsole.AUTH_SCOPE = ['friends_location', 'read_friendlists']

def retrieve_friends():
    fbconsole.authenticate()
    friends = fbconsole.get('/me/friends', {'fields':'id,first_name,last_name'})
    next_url = friends.get('paging')
    friends = friends['data']
    while next_url:
        p = fbconsole.urlparse(next_url['next'])
        more_friends = fbconsole.get(p.path+'?'+p.query)
        next_url = more_friends.get('paging')
        more_friends = more_friends['data']
        if not more_friends:
            break
        friends.extend(more_friends)
    return friends

def download_profile_pics(friends):
    print 'downloading profile pictures...'
    for f in friends:
        picture_url = '/%s/picture' % (f['id'],)
        profile_pic = fbconsole.graph_url(picture_url)
        img_path = u'/tmp/%s.jpg' % (f['id'],)
        if os.path.exists(img_path):
            f['img_path'] = img_path
            continue
        urllib.urlretrieve(profile_pic, img_path)
        print f['first_name'], f['last_name'], f['id']
        f['img_path'] = img_path
    return friends

def clean_tmp_pictures():
    for j in glob.glob('/tmp/*.jpg'):
        try:
            os.remove(j)
        except OSError, e:
            print j, e

class SearchConflictException(Exception):
    pass

def searchABBook(first, last):
    s = ABPerson.searchElementForProperty_label_key_value_comparison_(u'First', 
            None, None, first, kABEqualCaseInsensitive)
    ab = ABAddressBook.sharedAddressBook()
    entries = ab.recordsMatchingSearchElement_(s)
    ret = []
    for e in entries:
        if e.valueForProperty_(u'Last').lower() == last.lower():
            ret.append(e)
    if len(ret) > 1:
        raise SearchConflictException(
                "There are multiple %s %s, please resolve the conflict." % (
                    first, last))
    if ret:
        return ret[0]
    else:
        return None

# You can sync only for the people at certain location or for some friend list
def sync_address_book(friends, location, friend_list=u''):
    ab = ABAddressBook.sharedAddressBook()
    for f in friends:
        # filter out the location is not in new york
        try:
            user_entry = fbconsole.get('/%s' % (f['id']))
        except:
            continue
        if location:
            location_dict = user_entry.get('location')
            if not location_dict or not location_dict.get('name'):
                continue
            if not location in location_dict.get('name'):
                continue

        # create record only if it does not exists
        try:
            p = searchABBook(f['first_name'], f['last_name'])
        except SearchConflictException:
            # you can decide what to do if there is exactly the same first
            # name and last name in your existing address book
            continue
        if not p:
            p = ABPerson.alloc().init()
        img_data = NSData.dataWithContentsOfFile_(f['img_path'])
        p.setImageData_(img_data)
        p.setValue_forProperty_(f['first_name'], u'First')
        p.setValue_forProperty_(f['last_name'], u'Last')
        ab.addRecord_(p)
        print f['first_name'], f['last_name']
    ab.save()

def readABBook():
    ab = ABAddressBook.sharedAddressBook()
    ppl = ab.people()
    for p in ppl:
        if not p.valueForProperty_(u"First"):
            continue
        print p.valueForProperty_(u"First"), p.valueForProperty_(u"Last")

if __name__=='__main__':
    friends = retrieve_friends()
    friends = download_profile_pics(friends)

    sync_address_book(friends, u'Seattle')

    # you can clean the temporary files
    #clean_tmp_pictures()
