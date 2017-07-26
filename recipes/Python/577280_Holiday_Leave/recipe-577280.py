#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Are You still forgetting how many days of leave you have?
Your chief is cheating you?
You don't want to ask everyday & run calculator & compute?
This tool is for you!

   * nice chronological view
   * add/remove your free days
   * automatically computing
   * no external-db dependency
   * easy to maintain / develop / change
   * few lines of code 
"""

__author__ =  'farciarz'
__version__ = '0.01 alpha'

import sys, os
import time
import operator
import cPickle as pickle
import argparse

STATIC_P = 'history.p'
STATIC_T = "%a, %d-%m-%y %H:%M"
PROTOCOL = pickle.HIGHEST_PROTOCOL

OPERATORS = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.add,
    }

class Log:
    """
    Namespaced list container.
    """
    history = []
    
    @classmethod
    def base(cls):
        """
        Return a current holiday-base value.
        """
        return (item[0] for item in cls.history[::-1] \
                if item[0].startswith('*')).next()

    @classmethod
    def holidays(cls):
        """
        Calculate and return how many leaves day you have.
        """
        item = None
        holidays = 0
        for _tuple in cls.history[::-1]:
            item = _tuple[0]
            if item != cls.base():
                holidays = OPERATORS[item[0:1]](holidays, int(item[1:]))
            else:
                holidays = holidays + int(cls.base()[1:])
                break
        return holidays
    
    @classmethod
    def print_log(cls):
        """
        Show the view.
        """
        for _tuple in Log.history:
            print '\t'.join(_tuple)
        print '---------------------------'
        print '\t\t      ==', Log.holidays()
            
    @classmethod
    def save_log(cls):
        """
        Save the view into some pickle file.
        """
        output = open(STATIC_P, 'wb')
        pickle.dump(Log.history, output, protocol=PROTOCOL)
        output.close()


class Operate(argparse.Action):
    """
    Action, assistance class.
    """
    
    def __call__(self, parser, namespace, values, option_string=None):
        """
        Each action should call this logic.
        """
            
        dis_dict = {'--add': '+',
                    '--remove': '-',
                    '-a': '+',
                    '-rm': '-',
                    '--reset': '*'}
        #debug
        #print '%r %r %r' % (namespace, values, option_string)
        if option_string == '--reset':
            print 'Base reset to: ', values
            Log.history.append(('*' + str(values),
                               time.strftime(STATIC_T, time.gmtime())))
            Log.save_log()
        elif option_string == '--clear':
            Log.history = []
            Log.save_log()
            os.remove(STATIC_P)
            sys.exit('Clear all data...OK')
        else:
            try:
                Log.history.append((dis_dict[option_string] + str(values),
                                    time.strftime(STATIC_T, time.gmtime())))
            except KeyError:
                pass
            else:
                Log.save_log()
            Log.print_log()


class Leave(object):
    """
    This simple tool helps maintaining your holiday leave.
    """
    
    def __init__(self):
        """
        Prepare argparse & pickle.
        """
        
        # create the parser        
        parser = argparse.ArgumentParser(
            description=self.__class__.__doc__,
            argument_default=argparse.SUPPRESS)
        
        # add the arguments
        parser.add_argument('--add', '-a', type=int, dest='add', action=Operate,
                            help='add some free days', default=0)
        parser.add_argument('--remove', '-rm', type=int, dest='remove', action=Operate,
                            help='remove some free days', default=0)
        parser.add_argument('--reset', type=int, dest='reset',
                            action=Operate,
                            help='reset holiday base', default=26)
        parser.add_argument('--show', action=Operate, nargs='?',
                            help='show holiday changelog')
        parser.add_argument('--clear', action=Operate, nargs='?',
                            help='clear all logs')

        # create file | use the existing one
        try:
            Log.history = pickle.load(open('history.p', 'rb'))
        except IOError:
            output = open(STATIC_P, 'wb')
            Log.history = [('*' + \
                           str(int(raw_input('Your holiday base (int): '))),
                           time.strftime(STATIC_T, time.gmtime()))]
            pickle.dump( Log.history, output, protocol=PROTOCOL )
            output.close()
        finally:
            parser.parse_args()
            
if __name__ == '__main__':
    LEAVE = Leave()
