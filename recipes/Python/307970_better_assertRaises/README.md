###a better assertRaises() for unittest.py

Originally published: 2004-10-11 13:43:54
Last updated: 2008-07-30 10:39:19
Author: Trent Mick

When writing unit tests for Python using the standard unittest.py system the assertRaises() (aka failUnlessRaises()) method is used to test that a particular call raises the given exception. This recipe if for assertRaisesEx() that adds three things: (1) the ability to assert the raised exception's args; (2) the ability to test that the stringified exception matches a given regular expression; and (3) much better failure messages.