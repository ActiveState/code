import os, sys, getpass
import poplib # http://docs.python.org/library/poplib.html
from email.utils import parsedate_tz
import calendar
import datetime

# The main parameter
last_wanted = datetime.datetime(2009, 10, 5)
print last_wanted

# Your pop parameter
M = poplib.POP3('your pop server host')
M.user(getpass.getuser())
M.pass_(os.getenv('PASS'))

messages_ids = [ int(m.split()[0]) for m in M.list()[1]]
messages_ids.reverse()

print 'messages_cnt', len(messages_ids)

def get_last_message_id(messages_ids, M, last_wanted):
    for i in messages_ids:
        try:
            message_lines = M.top( str(i), '0')[1]
        except poplib.error_proto:
            print 'Problem in pop top call...'
            continue

        for line in message_lines:
            if line.startswith('Date:'):

                date_hdr = line.partition('Date: ')[2]
                # print date_hdr
                try:
                    (y, month, d, \
                     h, min, sec, \
                     _, _, _, tzoffset) = parsedate_tz(date_hdr)
                except (TypeError): continue
                except (ValueError): continue

                # Python range builtin ?
                if month < 0 or month > 12: continue
                max_day_per_month = max(calendar.monthcalendar(y, month)[-1])
                if d <= 0 or d > max_day_per_month: continue
                if h < 0 or h > 23: continue
                if min < 0 or min > 59: continue

                date = datetime.datetime(y, month, d, h, min, sec)

                print date
                if date < last_wanted:
                    return i

last_id = get_last_message_id(messages_ids, M, last_wanted)
messages_to_delete = [i for i in messages_ids if i < last_id]
print 'to delete', len(messages_to_delete)

for i in messages_to_delete:
    M.dele( str(i) )
M.quit()
