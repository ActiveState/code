## Timing an external subprocess

Originally published: 2008-09-24 11:34:52
Last updated: 2008-09-24 11:34:52
Author: Benjamin Hall

Running separate processes with os.system() has a single major disadvantage for the work I'm doing, and that is the external program is prone to entering a state where it stops producing any output. The "wallclock" subroutine runs an external command and periodically checks to see if it has finished, killing it if it runs for too long.