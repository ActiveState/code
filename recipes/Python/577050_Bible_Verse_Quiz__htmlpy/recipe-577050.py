#! /usr/bin/env python
"""Define several XHTML document strings to be used in VerseMatch.

Unlike the original program written in Java, a large portion of the
XHTML code is defined separately here to be used as format strings."""

################################################################################

__author__ = 'Stephen "Zero" Chappell <Noctis.Skytower@gmail.com>'
__date__ = '11 February 2010'
__version__ = '$Revision: 3 $'

################################################################################

TEMPLATE = '''\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml11-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <!-- Name: Stephen Paul Chappell -->
        <!-- Date: 4 February 2010       -->

        <meta name="author" content="Stephen Paul Chappell" />
        <meta name="classification" content="Verse Quiz Server" />
        <meta name="description" content="This is a Java-to-Python port." />

        <meta name="owner" content="Stephen Paul Chappell" />
        <meta name="copyright" content="&copy; 2010 Open Source" />
        <meta name="generator" content="Python IDLE" />
        <meta name="keywords" content="bible,verse,quiz,java,python,port" />

        <meta http-equiv="Content-Type" content="text/html;charset=ASCII" />
{}    
        <title>Simple "Verse Quiz" Servlet</title>
    </head>
    <body>
        <h1>Verse Quiz, by Stephen Paul Chappell</h1>
        <hr />
        <form id="GUI" name="GUI" method="POST">
            | |
            <input name="action" type="submit" value="Reset Session" />
            | |
{}
        </form>
    </body>
</html>'''

################################################################################

REFRESH = '''\
        <meta http-equiv="refresh" content="4;url=./?action=checkstatus" />
'''

################################################################################

GET_QUIZ = '''\
            <hr />
            <fieldset>
                <legend>Quiz Selection</legend>
                <h3>Choose one of the lists down below:</h3>
{}
                <input name="action" type="submit" value="Choose Quiz" />
            </fieldset>'''

################################################################################

GET_VERSE = '''\
            <input name="action" type="submit" value="Go Back" />
            | |
            <hr />
            <fieldset>
                <legend>Verse Selection</legend>
                <h3>Choose a verse from {}:</h3>
{}
            </fieldset>'''

################################################################################

TEACH = '''\
            <input name="action" type="submit" value="Go Back" />
            | |
            <hr />
{}
            <fieldset>
                <legend>Verse Entry Submission</legend>
                <h3>When you are done:</h3>
                <input name="action" type="submit" value="Check Your Answer" />
            </fieldset>'''

################################################################################

VERSE = '''\
            <fieldset>
                <legend>{0}</legend>{1}
                <textarea id="{2}" name="{2}" rows="5" cols="70">{3}</textarea>
            </fieldset>'''

################################################################################

CHECK = '''\
            <input name="action" type="submit" value="Reset Session" />
            | |
            <hr />
            <fieldset>
                <legend>Please Wait</legend>
                <h3>{} verse{} been graded so far.</h3>
            </fieldset>'''
