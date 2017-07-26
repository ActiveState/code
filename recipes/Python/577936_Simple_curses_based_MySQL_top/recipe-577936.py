#!/usr/bin/env python
# Stdlib imports
import os, sys
import time
import curses

# 3rd Party imports
import MySQLdb

def getStats(scr, db=None):
    (maxY, maxX) = scr.getmaxyx()
    sql = db.cursor()
    fp = open('debug', 'w+')
    maxInfo = (maxX-75)
    while 1:
        try:
            sql.execute('SHOW PROCESSLIST;')
            scr.addstr(0, 0, time.ctime())
            scr.addstr(1, 0, 'System Load: %s' % (str(os.getloadavg())[1:][:-1]))
            scr.addstr(3, 0, '%-10s %-20s %-15s %-8s %-8s %-5s%s' % (
                'User', 'Host', 'Db', 'Command', 'Time', 'Info', ' '*(maxX-71)), curses.A_BOLD|curses.A_REVERSE)
            cnt = 5
            try:
                for row in sql.fetchall():
                    if row[4].lower().strip() == 'query':
                        scr.addstr(cnt, 0, '%-10s %-20s %-15s %-8s %-8s %-5s' % (
                            row[1], row[2].split(':')[0], row[3], row[4], row[5], row[7]),
                            curses.A_BOLD)
                    else:
                        scr.addstr(cnt, 0, '%-10s %-20s %-15s %-8s %-8s %-5s' % (
                            row[1], row[2].split(':')[0], row[3], row[4], row[5], row[7]))
                    cnt += 1
                scr.addstr(cnt, 0, ' '*(maxX-1))
            except curses.error: pass
            except IOError: pass
            scr.move(maxY-2,maxX-2)
            scr.refresh()
            time.sleep(1.5)
            scr.erase()
        except KeyboardInterrupt:
            sys.exit(-1)

if __name__ == '__main__':
    try:
        db = MySQLdb.connect(sys.argv[1], user=sys.argv[2], passwd=sys.argv[3])
    except IndexError:
        print 'Usage: %s <host> <user> <passwd>' % os.path.basename(sys.argv[0])
        sys.exit(-1)
    curses.wrapper(getStats, db)
