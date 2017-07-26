#==============================================================================#
#  paratime.py                                                                 #
#==============================================================================#

"""Module for paratessares time conversions.

This module provides several functions that
covert earth seconds into paratessares time."""

################################################################################

__version__ = "$Revision: 3 $"
__date__ = "14 January 2009"
__author__ = "Stephen Chappell <Noctis.Skytower@gmail.com>"
__credits__ = """\
S. Schaub, for teaching me about interpreted languages.
D. Wooster, for teaching me about simulations and C#.
B. Gates, for allowing timers to be included with C#."""

################################################################################

import time as _time
import _thread
import sys as _sys

################################################################################

EPOCH_DELTA = 946684800
MICREV_IN_DAY = 1000000
MILREV_IN_DAY = 1000

SECOND_IN_DAY = 86400
DAY_IN_WEEK = 7
WEEK_IN_MONTH = 4
MONTH_IN_SEASON = 3
SEASON_IN_YEAR = 4

SECOND_IN_WEEK = SECOND_IN_DAY * DAY_IN_WEEK
SECOND_IN_MONTH = SECOND_IN_WEEK * WEEK_IN_MONTH
SECOND_IN_SEASON = SECOND_IN_MONTH * MONTH_IN_SEASON
SECOND_IN_YEAR = SECOND_IN_SEASON * SEASON_IN_YEAR

################################################################################

def seconds():
    "Return seconds since the epoch."
    return _time.time() - EPOCH_DELTA

def micrev(seconds):
    "Convert from seconds to micrev."
    x = seconds % SECOND_IN_DAY * MICREV_IN_DAY / SECOND_IN_DAY % MILREV_IN_DAY
    return int(x)

def milrev(seconds):
    "Convert from seconds to milrev."
    x = seconds % SECOND_IN_DAY * MILREV_IN_DAY / SECOND_IN_DAY
    return int(x)

def day(seconds):
    "Convert from seconds to days."
    x = seconds / SECOND_IN_DAY % DAY_IN_WEEK
    return int(x)

def week(seconds):
    "Convert from seconds to weeks."
    x = seconds / SECOND_IN_WEEK % WEEK_IN_MONTH
    return int(x)

def month(seconds):
    "Convert from seconds to months."
    x = seconds / SECOND_IN_MONTH % MONTH_IN_SEASON
    return int(x)

def season(seconds):
    "Convert from seconds to seasons."
    x = seconds / SECOND_IN_SEASON % SEASON_IN_YEAR
    return int(x)

def year(seconds):
    "Convert from seconds to years."
    x = seconds / SECOND_IN_YEAR
    return int(x)
    
################################################################################

UNITS = year, season, month, week, day, milrev, micrev

def text(seconds, spec='{0}.{1}.{2}.{3}.{4}.{5:03}.{6:03}', unit=UNITS):
    "Convert from seconds to text."
    return spec.format(*[func(seconds) for func in unit])

################################################################################

class Micrev_Timer:

    "Micrev_Timer(function, *args, **kwargs) -> Micrev_Timer"

    def __init__(self, function, *args, **kwargs):
        "Initialize the Micrev_Timer object."
        self.__function = function
        self.__args = args
        self.__kwargs = kwargs
        self.__thread = False
        self.__lock = _thread.allocate_lock()

    def start(self):
        "Start the Micrev_Timer object."
        with self.__lock:
            self.__active = True
            if not self.__thread:
                self.__thread = True
                _thread.start_new_thread(self.__run, ())

    def stop(self):
        "Stop the Micrev_Timer object."
        with self.__lock:
            self.__active = False

    def __run(self):
        "Private class method."
        start = _time.clock()
        timer = 0
        while True:
            timer += 1
            sleep = start + timer * 0.0864 - _time.clock()
            assert sleep >= 0, 'Function Was Too Slow'
            _time.sleep(sleep)
            with self.__lock:
                if not self.__active:
                    self.__thread = False
                    break
            self.__function(*self.__args, **self.__kwargs)

################################################################################

class Quantum_Timer:

    "Quantum_Timer(function, *args, **kwargs) -> Quantum_Timer"

    def __init__(self, function, *args, **kwargs):
        "Initialize the Quantum_Timer object."
        self.__function = function
        self.__args = args
        self.__kwargs = kwargs
        self.__thread = False
        self.__lock = _thread.allocate_lock()

    def start(self):
        "Start the Quantum_Timer object."
        with self.__lock:
            self.__active = True
            if not self.__thread:
                self.__thread = True
                _thread.start_new_thread(self.__run, ())

    def stop(self):
        "Stop the Quantum_Timer object."
        with self.__lock:
            self.__active = False

    def __run(self):
        "Private class method."
        while True:
            time = _time.clock()
            plus = time + 0.0864
            over = plus % 0.0864
            diff = plus - time - over
            _time.sleep(diff)
            with self.__lock:
                if not self.__active:
                    self.__thread = False
                    break
            self.__function(*self.__args, **self.__kwargs)

################################################################################

if __name__ == '__main__':
    _sys.stdout.write('Content-Type: text/plain\n\n')
    _sys.stdout.write(open(_sys.argv[0]).read())

#==============================================================================#
#  test_paratime.py                                                            #
#==============================================================================#

import paratime
import time
import datetime
import inspect
import unittest
from test import support

class ConstantTest(unittest.TestCase):

    def test_existance(self):
        # See if all required constants exist and do not equal zero.
        constants = ['EPOCH_DELTA', 'MICREV_IN_DAY', 'MILREV_IN_DAY',
                     'SECOND_IN_DAY', 'DAY_IN_WEEK', 'WEEK_IN_MONTH',
                     'MONTH_IN_SEASON', 'SEASON_IN_YEAR', 'SECOND_IN_WEEK',
                     'SECOND_IN_MONTH', 'SECOND_IN_SEASON', 'SECOND_IN_YEAR']
        for name in constants:
            self.assert_(hasattr(paratime, name), 'AttributeError: ' + name)
            CONSTANT = getattr(paratime, name)
            self.assert_(isinstance(CONSTANT, int), 'TypeError: ' + name)
            self.assert_(CONSTANT != 0, 'ValueError: ' + name)

    def test_epoch(self):
        # Ensure that EPOCH_DELTA is correct for this system.
        delta = paratime.EPOCH_DELTA
        epoch = time.gmtime(0)[:3]
        edate = datetime.date(*epoch)
        pdate = datetime.date(2000, 1, 1)
        days = (pdate - edate).days
        seconds = days * 24 * 60 * 60
        self.assert_(delta == seconds, 'ValueError: EPOCH_DELTA')

    def test_division(self):
        # Check that the daily divisions have not changed.
        micrev = paratime.MICREV_IN_DAY
        milrev = paratime.MILREV_IN_DAY
        second = paratime.SECOND_IN_DAY
        self.assert_(micrev == 10 ** 6, 'ValueError: MICREV_IN_DAY')
        self.assert_(milrev == 10 ** 3, 'ValueError: MILREV_IN_DAY')
        self.assert_(second == 24 * 60 * 60, 'ValueError: SECOND_IN_DAY')

    def test_year(self):
        # Use various checksums to verify the design of a year.
        d = paratime.DAY_IN_WEEK
        w = paratime.WEEK_IN_MONTH
        m = paratime.MONTH_IN_SEASON
        s = paratime.SEASON_IN_YEAR
        self.assert_(d ^ w ^ m ^ s == 4, 'ValueError: XOR')
        self.assert_(d + w + m + s == 18, 'ValueError: Addition')
        self.assert_(d * w * m * s == 336, 'ValueError: Multiplication')
        self.assert_(hash((d, w, m, s)) == 1672362005, 'ValueError: Hash')

    def test_second(self):
        # Test that the dynmaic constants were created correctly.
        week = paratime.SECOND_IN_WEEK
        month = paratime.SECOND_IN_MONTH
        season = paratime.SECOND_IN_SEASON
        year = paratime.SECOND_IN_YEAR
        self.assert_(week == 604800, 'ValueError: SECOND_IN_WEEK')
        self.assert_(month == 2419200, 'ValueError: SECOND_IN_MONTH')
        self.assert_(season == 7257600, 'ValueError: SECOND_IN_SEASON')
        self.assert_(year == 29030400, 'ValueError: SECOND_IN_YEAR')

    def test_unit(self):
        # Examine the constant UNITS for proper compostion.
        functions = ['year', 'season', 'month', 'week', 'day',
                     'milrev', 'micrev']
        self.assert_(hasattr(paratime, 'UNITS'), 'AttributeError: UNITS')
        istuple = isinstance(getattr(paratime, 'UNITS'), tuple)
        self.assert_(istuple, 'TypeError: UNITS')
        units = tuple(getattr(paratime, name) for name in functions)
        self.assert_(paratime.UNITS == units, 'ValueError: UNITS')

class FunctionTest(unittest.TestCase):

    def test_existance(self):
        # Make sure that all required functions exist.
        functions = ['seconds', 'micrev', 'milrev',
                     'day', 'week', 'month', 'season', 'year',
                     'text']
        for name in functions:
            self.assert_(hasattr(paratime, name), 'AttributeError: ' + name)
            isfunction = inspect.isfunction(getattr(paratime, name))
            self.assert_(isfunction, 'TypeError: ' + name)

    def test_zero(self):
        # Test that argument 0.0 always returns 0.0 from functions.
        functions = ['micrev', 'milrev',
                     'day', 'week', 'month', 'season', 'year']
        for name in functions:
            func = getattr(paratime, name)
            self.assert_(func(0.0) == 0.0, 'ArithmeticError: ' + name)

    def test_year(self):
        # Find out if proper mathamatical divisions exist in a year.
        functions = ['day', 'week', 'month', 'season']
        for name in functions:
            func = getattr(paratime, name)
            constant = 'SECOND_IN_' + name.upper()
            CONSTANT = getattr(paratime, constant)
            self.assert_(func(CONSTANT) == 1, 'ArithmeticError: ' + name)
            self.assert_(func(CONSTANT - 1) == 0, 'ArithmeticError: ' + name)

    def test_rev(self):
        # Check that partioning of the day is computed correctly.
        micrev = paratime.micrev
        milrev = paratime.milrev
        test_mic = lambda s: int(s * 1000000 / 86400 % 1000)
        test_mil = lambda s: int(s * 1000 / 86400 % 1000)
        for s in range(int(24 * 60 * 60 * 1.01)):
            self.assert_(micrev(s) == test_mic(s), 'ArithmeticError: micrev')
            self.assert_(milrev(s) == test_mil(s), 'ArithmeticError: milrev')

class TextTest(unittest.TestCase):

    def setUp(self):
        # Create some variables to help with the upcoming tests.
        self.T = paratime.text
        self.S = [10344926.962133339, 94639768.804546028, 265532741.01112196,
                  16253695.553989811, 108469967.14143418, 268212543.20094055,
                  56911478.644419812, 135376331.24554729, 300908237.98332906,
                  63510559.911042809, 137084486.30913293, 373636131.91095936,
                  72101267.095945552, 140265693.15057722, 380887195.47359467,
                  78426890.295372367, 146538409.07728666, 404198696.61584091,
                  83581780.421440393, 197104443.98377159, 405806804.27733558,
                  85208640.256408677, 217453332.36529338, 410940507.48093152,
                  88576536.868952677, 232335476.22987685, 411771351.90179437,
                  90854227.747951403, 263271517.23457572, 412037865.73197347]

    def test_seconds(self):
        # Ensure that the default settings work properly.
        keys = ['0.1.1.1.0.732.950', '3.1.0.0.3.367.694', '9.0.1.3.0.295.613',
                '0.2.0.2.6.121.476', '3.2.2.3.2.439.434', '9.0.2.3.3.311.842',
                '1.3.2.2.0.697.669', '4.2.1.3.5.855.685', '10.1.1.1.3.734.235',
                '2.0.2.1.0.075.924', '4.2.2.2.4.625.998', '12.3.1.1.5.492.267',
                '2.1.2.3.1.505.406', '4.3.0.3.6.445.522', '13.0.1.1.5.416.614',
                '2.2.2.1.4.718.637', '5.0.0.2.2.046.401', '13.3.2.0.2.225.655',
                '2.3.1.2.1.381.717', '6.3.0.1.6.301.434', '13.3.2.2.6.838.012',
                '2.3.2.0.6.211.114', '7.1.2.3.3.820.976', '14.0.1.3.3.255.873',
                '3.0.0.2.3.191.398', '8.0.0.0.1.068.011', '14.0.2.0.5.872.128',
                '3.0.1.2.1.553.561', '9.0.0.3.2.124.042', '14.0.2.1.1.956.779']
        for seconds, results in zip(self.S, keys):
            self.assert_(self.T(seconds) == results, 'ValueError: Default')

    def test_spec(self):
        # Check that various format specifications do not cause errors.
        form = ['Year = {0}', 'Season = {1}', 'Month = {2}', 'Week = {3}',
                'Day = {4}', 'Milrev = {5:03}', 'Micrev = {6:03}',
                'Season {1} of Year {0}', 'Month {2} of Season {1}',
                'Week {3} of Month {2}', 'Day {4} of Week {3}',
                'The time is {5}:{6}.', 'This is year {0}.']
        keys = ['0 1 1 1 0 732 950 10 11 11 01 732:950 0',
                '3 1 0 0 3 367 694 13 01 00 30 367:694 3',
                '9 0 1 3 0 295 613 09 10 31 03 295:613 9',
                '0 2 0 2 6 121 476 20 02 20 62 121:476 0',
                '3 2 2 3 2 439 434 23 22 32 23 439:434 3',
                '9 0 2 3 3 311 842 09 20 32 33 311:842 9',
                '1 3 2 2 0 697 669 31 23 22 02 697:669 1',
                '4 2 1 3 5 855 685 24 12 31 53 855:685 4',
                '10 1 1 1 3 734 235 110 11 11 31 734:235 10',
                '2 0 2 1 0 075 924 02 20 12 01 75:924 2',
                '4 2 2 2 4 625 998 24 22 22 42 625:998 4',
                '12 3 1 1 5 492 267 312 13 11 51 492:267 12',
                '2 1 2 3 1 505 406 12 21 32 13 505:406 2',
                '4 3 0 3 6 445 522 34 03 30 63 445:522 4',
                '13 0 1 1 5 416 614 013 10 11 51 416:614 13',
                '2 2 2 1 4 718 637 22 22 12 41 718:637 2',
                '5 0 0 2 2 046 401 05 00 20 22 46:401 5',
                '13 3 2 0 2 225 655 313 23 02 20 225:655 13',
                '2 3 1 2 1 381 717 32 13 21 12 381:717 2',
                '6 3 0 1 6 301 434 36 03 10 61 301:434 6',
                '13 3 2 2 6 838 012 313 23 22 62 838:12 13',
                '2 3 2 0 6 211 114 32 23 02 60 211:114 2',
                '7 1 2 3 3 820 976 17 21 32 33 820:976 7',
                '14 0 1 3 3 255 873 014 10 31 33 255:873 14',
                '3 0 0 2 3 191 398 03 00 20 32 191:398 3',
                '8 0 0 0 1 068 011 08 00 00 10 68:11 8',
                '14 0 2 0 5 872 128 014 20 02 50 872:128 14',
                '3 0 1 2 1 553 561 03 10 21 12 553:561 3',
                '9 0 0 3 2 124 042 09 00 30 23 124:42 9',
                '14 0 2 1 1 956 779 014 20 12 11 956:779 14']
        table = str.maketrans('', '', ' .=DMSTWYacefhiklmnorstvy')
        clean = lambda S: S.translate(table)
        for seconds, results in zip(self.S, keys):
            for spec, result in zip(form, results.split()):
                purged = clean(self.T(seconds, spec))
                self.assert_(purged == result, 'ValueError: Format')

    def test_unit(self):
        # Try running through several custom unit combinations.
        days = lambda x: int(x / 86400)
        hours = lambda x: int(x / 3600) % 24
        minutes = lambda x: int(x / 60) % 60
        seconds = lambda x: int(x) % 60
        args = [('D{0}', [days]),
                ('H{0}', [hours]),
                ('M{0}', [minutes]),
                ('S{0}', [seconds]),
                ('{0}:{1:02}:{2:02}:{3:02}', [days, hours, minutes, seconds])]
        keys = ['119 17 35 26 119173526', '1095 8 49 28 1095084928',
                '3073 7 5 41 3073070541', '188 2 54 55 188025455',
                '1255 10 32 47 1255103247', '3104 7 29 3 3104072903',
                '658 16 44 38 658164438', '1566 20 32 11 1566203211',
                '3482 17 37 17 3482173717', '735 1 49 19 735014919',
                '1586 15 1 26 1586150126', '4324 11 48 51 4324114851',
                '834 12 7 47 834120747', '1623 10 41 33 1623104133',
                '4408 9 59 55 4408095955', '907 17 14 50 907171450',
                '1696 1 6 49 1696010649', '4678 5 24 56 4678052456',
                '967 9 9 40 967090940', '2281 7 14 3 2281071403',
                '4696 20 6 44 4696200644', '986 5 4 0 986050400',
                '2516 19 42 12 2516194212', '4756 6 8 27 4756060827',
                '1025 4 35 36 1025043536', '2689 1 37 56 2689013756',
                '4765 20 55 51 4765205551', '1051 13 17 7 1051131707',
                '3047 2 58 37 3047025837', '4768 22 57 45 4768225745']
        prefix = ['D', 'H', 'M', 'S', '']
        finish = lambda S: ':'.join((S[:-6], S[-6:-4], S[-4:-2], S[-2:]))
        for seconds, results in zip(self.S, keys):
            for unit, plus, result in zip(args, prefix, results.split()):
                ans = self.T(seconds, *unit)
                key = (plus + result) if plus else finish(result)
                self.assert_(ans == key, 'ValueError: Functions')

class TimerTest(unittest.TestCase):

    def test_fast(self):
        # Check that quick functions can be run without failing.
        MT = self.timer(self.increment, 0.0625)
        MT.start()
        time.sleep(0.5)
        MT.stop()
        time.sleep(0.25)
        self.assert_(self.fast(), 'ValueError: Count')

    def test_slow(self):
        # Verify the behavior of the timer's thread under load.
        MT = self.timer(self.increment, 0.125)
        with support.captured_output('stderr') as stderr:
            MT.start()
            time.sleep(0.5)
            MT.stop()
            time.sleep(0.25)
        self.assert_(self.slow(), 'ValueError: Count')
        self.assert_(self.test(stderr.getvalue()), 'IOError: Thread')

    def increment(self, seconds):
        # Keep track of how many times the thread runs.
        time.sleep(seconds)
        self.count += 1

class MicrevTest(TimerTest):

    def setUp(self):
        # Create variables specifically for testing Micrev_Timer.
        self.count = 0
        self.timer = paratime.Micrev_Timer
        self.fast = lambda: self.count == 5
        self.slow = lambda: self.count == 1
        self.test = lambda S: 'Function Was Too Slow' in S

class QuantumTest(TimerTest):

    def setUp(self):
        # Create variables specifically for testing Quantum_Timer.
        self.count = 0
        self.timer = paratime.Quantum_Timer
        self.fast = lambda: 5 <= self.count <= 6
        self.slow = lambda: self.count == 3
        self.test = lambda S: len(S) == 0

def test_main():
    support.run_unittest(ConstantTest,
                         FunctionTest, TextTest,
                         MicrevTest, QuantumTest)

if __name__ == '__main__':
    test_main()

#==============================================================================#
#  Clock.pyw                                                                   #
#==============================================================================#

import tkinter
import paratime

def main():
    root = tkinter.Tk()
    root.resizable(False, False)
    root.title('Time in Tessaressunago')
    time = tkinter.StringVar()
    text = tkinter.Label(textvariable=time, font=('helvetica', 16, 'bold'))
    text.grid(padx=5, pady=5)
    thread = paratime.Quantum_Timer(update, time)
    thread.start()
    root.mainloop()

def update(time):
    s = paratime.seconds()
    t = paratime.text(s)
    p = 1000000000 * 1.01 ** (s / paratime.SECOND_IN_YEAR)
    time.set('Time = {0}\nNational = {1}'.format(t, fix(p)))

def fix(number, sep=','):
    number = str(int(number))
    string = ''
    while number:
        string = number[-1] + string
        number = number[:-1]
        if number and not (len(string) + 1) % 4:
            string = sep + string
    return string

if __name__ == '__main__':
    main()

#==============================================================================#
#  BACKUP 3.0.py                                                               #
#==============================================================================#

from getpass import getuser
from paratime import seconds, text
import os

###############################################################################

GET = os.path.join('C:\\Documents and Settings', getuser(), 'My Documents')
SET = os.path.join('G:\\BACKUP', text(seconds()))

JUNK_FILE = 'Thumbs.db', 'Desktop.ini'
JUNK_EXT = 'pyc', 'pyo'

###############################################################################

def main():
    prune_junk()
    prune_dirs()
    backup_dirs(GET, SET)
    show_prompt()

def show_prompt():
    if WARNINGS:
        print('====================')
        print('Warnings Will Follow')
        input('====================')
        for warning in WARNINGS:
            print('ERROR: ', warning)
    print('==================')
    print('Backup Is Complete')
    input('==================')

###############################################################################

JUNK_FILE = [name.lower() for name in JUNK_FILE]
JUNK_EXT = ['.' + name.lower() for name in JUNK_EXT]

def prune_junk():
    for root, dirs, files in os.walk(GET):
        for name in files:
            path = name.lower()
            if path in JUNK_FILE or os.path.splitext(path)[1] in JUNK_EXT:
                path = os.path.join(root, name)
                os.remove(path)
                print('REMOVE:', path)

def prune_dirs():
    for root, dirs, files in os.walk(GET, False):
        for name in dirs:
            path = os.path.join(root, name)
            if empty(path):
                os.rmdir(path)
                print('RMDIR: ', path)

def empty(path):
    for name in os.listdir(path):
        path_name = os.path.join(path, name)
        if os.path.isdir(path_name) and not empty(path_name):
            return False
        elif os.path.isfile(path_name):
            return False
        return True

###############################################################################

WARNINGS = []

def backup_dirs(source, destination):
    contents = os.listdir(source)
    os.mkdir(destination)
    print('MKDIR: ', destination)
    for name in contents:
        source_name = os.path.join(source, name)
        destination_name = os.path.join(destination, name)
        try:
            if os.path.isdir(source_name):
                backup_dirs(source_name, destination_name)
            elif os.path.isfile(source_name):
                backup_file(source_name, destination_name)
        except:
            WARNINGS.append(source_name)

def backup_file(source, destination):
    sour = open(source, 'rb')
    dest = open(destination, 'wb')
    print('OPEN:  ', destination)
    buff = sour.read(1 << 20)
    while buff:
        dest.write(buff)
        buff = sour.read(1 << 20)
    sour.close()
    dest.close()

###############################################################################

if __name__ == '__main__':
    main()
