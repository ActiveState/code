#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import codecs
import csv
import re
import urlparse
import itertools
import cStringIO

GMAIL_CSV_HEADER_FIELDS = (
    'Name',
    'E-mail',
    'Notes',
)
GMAIL_CSV_SECTION_FIELDS = (
    'Description',
    'Email',
    'IM',
    'Phone',
    'Mobile',
    'Pager',
    'Fax',
    'Company',
    'Title',
    'Other',
    'Address',
)

# gnokii raw format constants
# format: ENTRY_NUMBER.NUMBER_x or ENTRY_x.0
# copied from include/gnokii/common.h
GN_NUMBER_HOME    = 0x02
GN_NUMBER_MOBILE  = 0x03
GN_NUMBER_FAX     = 0x04
GN_NUMBER_WORK    = 0x06
GN_NUMBER_GENERAL = 0x0a

GN_ENTRY_NAME       = 0x07
GN_ENTRY_EMAIL      = 0x08
GN_ENTRY_POSTAL     = 0x09
GN_ENTRY_NOTE       = 0x0a
GN_ENTRY_NUMBER     = 0x0b
GN_ENTRY_RINGTONE   = 0x0c
GN_ENTRY_DATE       = 0x13   # Date is used for DC,RC,etc (last calls)
GN_ENTRY_POINTER    = 0x1a   # Pointer to the other memory
GN_ENTRY_LOGO       = 0x1b
GN_ENTRY_LOGOSWITCH = 0x1c
GN_ENTRY_GROUP      = 0x1e
GN_ENTRY_URL        = 0x2c
GN_ENTRY_RINGTONEADV= 0x37

# Mappings from gmail to gnokii in
# ((gmail_section, gmail_field), (gnokii_entry, gnokii_number))
# format.
# None is wildcard. Order matters, list most specific first
FIELD_PAIR = (
    (('Home', 'Phone'),(GN_ENTRY_NUMBER, GN_NUMBER_HOME)),
    ((None, 'Mobile'), (GN_ENTRY_NUMBER, GN_NUMBER_MOBILE)),
    ((None, 'Fax'),    (GN_ENTRY_NUMBER, GN_NUMBER_FAX)),
    (('Work', 'Phone'),(GN_ENTRY_NUMBER, GN_NUMBER_WORK)),
    ((None,   'Phone'),  (GN_ENTRY_NUMBER, GN_NUMBER_GENERAL)),
    ((None, 'Name'),   (GN_ENTRY_NAME, 0)),# special case, is primary key
    ((None, 'E-mail'), (GN_ENTRY_EMAIL, 0)),
    ((None, 'Email'), (GN_ENTRY_EMAIL, 0)),# they should just pick one spelling
    ((None, 'Address'),(GN_ENTRY_POSTAL, 0)),
    ((None, 'Notes'),  (GN_ENTRY_NOTE, 0)),
)

def field_match(section, field):
    '''field_match(None, "Name") -> (GN_ENTRY_NAME, 0)
    returns None when not found'''
    # naive linear scan of patterns
    for ((s, f), (e, n)) in FIELD_PAIR:
        if field == f and (s == None or s == section):
            return (e, n)
    else: # not found
        return None

def field_extract_section(field):
    m = re.compile(r'Section (\d+) -').match(field)
    sec = None
    if m:
        sec = int(m.group(1))
        (i, j) = m.span()
        field = field[j:].strip()
    return (sec, field)

def get_item(l, index):
    try:
        return l[index]
    except IndexError:
        return ''

def is_url(s):
    (s, h) = urlparse.urlparse(s)[:2]
    return s and h

def phone_number_filter(s):
    out = []
    for i in s:
        if i.isdigit():
            out.append(i)
    return ''.join(out)

def isspace_to_space(s):
    out = []
    for i in s:
        if i.isspace():
            out.append(' ')
        else:
            out.append(i)
    return ''.join(out)

def transform(field_to_sec_field, section_description_fields, csv_record):
    def split_value(value):
        for i in value.split(':::'):
            i = i.strip()
            if i:
                yield isspace_to_space(i) # FIXME: hackish
    sec_num_to_section = [ None ] + list( get_item(csv_record,i)
        for i in section_description_fields )
    for (i, v) in enumerate(csv_record):
        if not v:
            continue
        (sec_num, field) = field_to_sec_field[i]
        try:
            section = sec_num_to_section[sec_num]
        except TypeError:
            section = None
        t = field_match(section, field)

        (entry, number) = (None, 0)
        if t:
            (entry, number) = t
        elif field == 'Other':
            for j in split_value(v):
                if is_url(j):
                    yield (GN_ENTRY_URL, 0, j)
                else:
                    yield (GN_ENTRY_NOTE, 0, j)

        if entry:
            for j in split_value(v):
                if entry == GN_ENTRY_NUMBER:
                    yield (entry, number, phone_number_filter(j))
                else:
                    yield (entry, number, j)

def iter_first(iterable):
    try:
        return iter(iterable).next()
    except StopIteration:
        return '' #FIXME: all my data are strings ...

def guess_primary_number(entry_list):
    #FIXME: should find a way to let user specify this in the Gmail CSV format
    'guess_primary_number( [ (e, n, v), ... ] ) -> v'
    l = list(entry_list)
    number_priority = (
        GN_NUMBER_MOBILE,
        GN_NUMBER_HOME,
        GN_NUMBER_WORK,
        GN_NUMBER_GENERAL,
    )
    d = dict( (v,i) for (i,v) in enumerate(number_priority) )
    l.sort(key=lambda (e,n,v): d.get(n, len(d)))
    try:
        return l[0][2]
    except IndexError:
        return ''

def gnokii_raw_gen(entry_list):
    name_entry = iter_first( (e, n, v) for (e, n, v) in entry_list
            if e == GN_ENTRY_NAME)
    if not name_entry:
        return ()
    entry_list.remove(name_entry)
    name = name_entry[2]
    primary_number = guess_primary_number( (e, n, v)
            for (e, n, v) in entry_list if e == GN_ENTRY_NUMBER )
    return (name, primary_number, entry_list)

def gnokii_write_phone_book(fout, phone_book):
    cl = csv.writer(fout, delimiter=';', lineterminator='\n')
    for (person_counter,(name, primary_number, entry_list)) in enumerate(phone_book):
        h =  [ name,
                primary_number,
                'ME', #mem_type, (ME: phone, SM: SIM card)
                person_counter+1, #mem_index, counts from 1
                5, #call_group, (5: not in any group)
            ]
        entries = []
        for (i, (e, n, v)) in enumerate(entry_list):
            entries.extend([e, n,
                    i+2, # entry counter, got the 2 starting value by experiment
                    v])
        cl.writerow(h + entries)

class UTF8Lines(object):
    '''Work around UnicodeEncodingError when using unicode with the csv module,
    just encode the data to utf-8.'''
    def __init__(self, fin):
        self.fin = fin
    def next(self):
        l = self.fin.readline()
        if l:
            return l.encode('utf-8')
        else:
            raise StopIteration
    def __iter__(self):
        return self

def gmail_csv_unicode_open(fin):
    'only supports utf-16 and utf-8'
    # byte order mark
    t = fin.read(2)
    if t == codecs.BOM_UTF16_LE:
        return UTF8Lines(codecs.getreader('utf-16le')(fin))
    elif t == codecs.BOM_UTF16_BE:
        return UTF8Lines(codecs.getreader('utf-16be')(fin))
    else: # assume utf-8
        l = fin.readline()
        return itertools.chain([ t + l ], fin)

def gmail_csv_to_gnokii(fin, fout):
    data = csv.reader(gmail_csv_unicode_open(fin))
    it = iter(data)
    fields = it.next() # first line is field names

    (field_to_sec_field, sec_description_fields) = ([], [])
    for (i, f) in enumerate(fields):
        (sec_num, f) = field_extract_section(f)
        field_to_sec_field.append((sec_num, f))
        if f == 'Description':
            sec_description_fields.append(i)
    phone_book = list( list(transform(field_to_sec_field, sec_description_fields, x))
            for x in it )
    phone_book.sort()

    gnokii_raw_data = filter(None, (gnokii_raw_gen(list(x)) for x in phone_book) )
    gnokii_write_phone_book(fout,  gnokii_raw_data)

GMAIL_CSV_EXAMPLE = (
','.join([ 'Name', 'E-mail', 'Notes', 'Section 1 - Description',
    'Section 1 - Email', 'Section 1 - IM', 'Section 1 - Phone',
    'Section 1 - Mobile', 'Section 1 - Pager', 'Section 1 - Fax',
    'Section 1 - Company', 'Section 1 - Title', 'Section 1 - Other',
    'Section 1 - Address', 'Section 2 - Description', 'Section 2 - Email',
    'Section 2 - IM', 'Section 2 - Phone', 'Section 2 - Mobile',
    'Section 2 - Pager', 'Section 2 - Fax', 'Section 2 - Company',
    'Section 2 - Title', 'Section 2 - Other', 'Section 2 - Address\n',
]) + ','.join([
    'Scott Tsai', 'scottt.tw@nospam', 'Scott Tsai', 'Personal',
    'email1@nospam ::: mail2@nospam', '', '', '123456789', '', '', '', '', '', '',
    '\n'
]))
GNOKII_EXAMPLE = ';'.join(
['Scott Tsai', '123456789', 'ME', '1', '5', '8', '0', '2', 'scottt.tw@nospam',
 '10', '0', '3', 'Scott Tsai', '8', '0', '4', 'email1@nospam', '8', '0', '5',
 'mail2@nospam', '11', '3', '6', '123456789\n'])
def test():
    assert field_match(None, 'Name') == (GN_ENTRY_NAME, 0)
    s = 'Phone'
    assert field_match('Work', s) == (GN_ENTRY_NUMBER, GN_NUMBER_WORK)
    assert field_match('Home', s) == (GN_ENTRY_NUMBER, GN_NUMBER_HOME)
    assert field_match('Other', s) == (GN_ENTRY_NUMBER, GN_NUMBER_GENERAL)

    out = cStringIO.StringIO()
    gmail_csv_to_gnokii(cStringIO.StringIO(GMAIL_CSV_EXAMPLE), out)
    out.seek(0)
    assert out.read() == GNOKII_EXAMPLE

def main(args):
    if not args:
        gmail_csv_to_gnokii(sys.stdin, sys.stdout)
    else:
        for i in args:
            (fin, fout) = (file(i, 'ra'),
                    file(os.path.splitext(i)[0]+'.gnokii_raw', 'wa'))
            gmail_csv_to_gnokii(fin, fout)

if __name__ == '__main__':
    main(sys.argv[1:])
