#!/usr/bin/env python

"""
Beep on me in a while.

Command line utility to shedule an alarm in a specified number of
minutes.

Need `beep <https://github.com/johnath/beep/>`_ on a GNU/Linux system.

    usage: alarm [-h] [-b "<options>"] [-a] number

    Beep-alarm in some minutes

    positional arguments:
      number                Number of minutes until alarm.

    optional arguments:
      -h, --help            show this help message and exit
      -b "<options>", --beep-options "<options>"
                            The options to provide to the beep command. See man
                            beep. Default: "-l 200 -d 50 -r 5"
      -a, --asynch          If given - start beep in the background

"""
import argparse
import os

description = ('Beep-alarm in some minutes')

parser = argparse.ArgumentParser(description=description)

boptsdef = '-l 200 -d 50 -r 5'

parser.add_argument('-b', '--beep-options', metavar='"<options>"',
                    dest='beep_opts', default=boptsdef,
                    help=('The options to provide to the beep command. '
                          'See man beep. Default: "' + boptsdef + '"'))

parser.add_argument(dest='minutes', metavar='number', type=float,
                    help=('Number of minutes until alarm.'))

parser.add_argument('-a', '--asynch', dest='asynch', action='store_true',
                    help='If given - start beep in the background')

args = parser.parse_args()

print 'minutes =', args.minutes
print 'beep_opts =', args.beep_opts
print 'asynch =', args.asynch

ms = str(args.minutes * 60000)
bg = ''
if args.asynch:
    bg = ' &'

os.system('beep -l 0 -D ' + ms + ' --new ' + args.beep_opts + bg)
