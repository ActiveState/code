#!/usr/bin/env python
import os, sys, time
import curses,struct

states = ['STARTUP', 'BLOCKED', 'CONNECT', 'PREPROCESS', 'SEND', 'COMPILE', 'RECEIVE', 'DONE']
DISTCC_DIR = os.getenv('DISTCC_DIR') or '%s/.distcc' % os.getenv('HOME')

def write(win=None, line=None, col=None, txt=None, attrs=None):
    if win != None:
        win.move(line, col)
        win.clrtoeol()
        win.addstr(line, col, txt, attrs)

def display_time(scr):
    t = time.ctime().split()
    write(scr, 0, 0,  t[0], curses.color_pair(9))
    write(scr, 0, 4,  t[1], curses.color_pair(9))
    write(scr, 0, 8,  t[2], curses.color_pair(9))
    write(scr, 0, 11, t[3], curses.color_pair(9))
    write(scr, 0, 20, t[4], curses.color_pair(9))

def display_loadavg(scr):
    lavg = os.getloadavg()
    write(scr, 1, 0, 'System',             curses.color_pair(9))
    write(scr, 1, 7, 'Load:',              curses.color_pair(9))
    write(scr, 1, 13, '%.02f' % lavg[0],   curses.color_pair(9))
    write(scr, 1, 20, '%.02f' % lavg[1],   curses.color_pair(9))
    write(scr, 1, 27, '%.02f' % lavg[2],   curses.color_pair(9))

def display_header(scr):
    write(scr, 3, 0,  'Slot',  curses.A_BOLD)
    write(scr, 3, 5,  'Host',  curses.A_BOLD)
    write(scr, 3, 25, 'State', curses.A_BOLD)
    write(scr, 3, 45, 'Filename', curses.A_BOLD)
    #'%-4s %-20s %-15s %-40s%s' % ('Slot', 'Remote Host', 'State', 'Filename', ' '*(maxX-83)), curses.A_BOLD)

def getStats(scr):
    curses.init_pair(9,  curses.COLOR_WHITE,  curses.COLOR_BLACK)
    curses.init_pair(10, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(11, curses.COLOR_RED,    curses.COLOR_BLACK)
    curses.init_pair(12, curses.COLOR_GREEN,  curses.COLOR_BLACK)
    (maxY, maxX) = scr.getmaxyx()
    while 1:
        try:
            display_time(scr)
            display_loadavg(scr)
            display_header(scr)
            #write(scr, 3, 0, '%-4s %-20s %-15s %-40s%s' % ('Slot', 'Remote Host', 'State', 'Filename', ' '*(maxX-83)), curses.A_BOLD)
            cnt = 5
            try:
                for i in os.listdir(DISTCC_DIR+'/state'):
                    data = struct.unpack('@iLL128s128siiP', open(DISTCC_DIR+'/state/'+i).readline().strip())
                    file = data[3].split('\x00')[0] or 'None'
                    host = data[4].split('\x00')[0] or 'None'
                    slot = int(data[5])
                    stte = states[int(data[6])]
                    scr.move(cnt,0)
                    scr.clrtoeol()
                    if 'None' not in (file, host):
                        write(scr, cnt, 0, '%s' % slot, curses.color_pair(9))
                        write(scr, cnt, 5, '%s' % host, curses.color_pair(9))
                        if int(data[6]) in (2,3):
                            write(scr, cnt, 25, '%s ' % (stte), curses.color_pair(10))
                        elif int(data[6]) in (0,1):
                            write(scr, cnt, 25, '%s ' % (stte), curses.color_pair(11))
                        elif int(data[6]) in (4,5):
                            write(scr, cnt, 25, '%s ' % (stte), curses.color_pair(12))
                        elif int(data[6]) in (6,7):
                            write(scr, cnt, 25, '%s ' % (stte), curses.color_pair(12)|curses.A_BOLD)
                        else: write(scr, cnt, 25, '%s ' % (stte))
                        write(scr, cnt, 45, '%s' % file, curses.color_pair(9))
                        cnt += 1
            except struct.error: pass
            except IOError: pass
            scr.refresh()
            time.sleep(0.75)
            scr.erase()
            scr.move(0,0)
        except KeyboardInterrupt:
            sys.exit(-1)

if __name__ == '__main__':
    curses.wrapper(getStats)
