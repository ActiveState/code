###Using terminfo for portable color output & cursor control

Originally published: 2006-03-11 14:06:33
Last updated: 2006-03-27 19:20:16
Author: Edward Loper

The curses module defines several functions (based on terminfo) that can be used to perform lightweight cursor control & output formatting (color, bold, etc).  These can be used without invoking curses mode (curses.initwin) or using any of the more heavy-weight curses functionality.  This recipe defines a TerminalController class, which can make portable output formatting very simple.  Formatting modes that are not supported by the terminal are simply omitted.