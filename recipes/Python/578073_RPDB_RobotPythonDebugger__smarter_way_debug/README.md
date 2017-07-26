## RPDB (RobotPythonDebugger) -- a smarter way to debug robotframework tests

Originally published: 2012-03-14 15:11:42
Last updated: 2012-03-14 15:12:39
Author: Daniel Cohn

Robotframework (http://code.google.com/p/robotframework/) is a tool used to run functional tests against a variety of targets.  Tests are organized in the form of keyword tsv or html files, which map input parameters to keyword-argument methods in the test suite.  Robot includes a fairly advanced logging mechanism, which is cool -- until you try to debug anything.  Debugging is made difficult because robot steals stdin and stdout when it is run, which means bye-bye debugging in the terminal.  rpdb solves this in a KISS simple way.