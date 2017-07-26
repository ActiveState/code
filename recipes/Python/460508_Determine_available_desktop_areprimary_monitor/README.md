## Determine the available desktop area (primary monitor) on Windows

Originally published: 2005-12-02 07:50:39
Last updated: 2005-12-02 07:50:39
Author: Martin Dengler

This recipe is the Python implementation of the SystemParametersInfoA() invocation required to retrieve the area that application windows can inhabit.  On multi-monitor setups, the windows code returns the area on the primary monitor only.  This recipe is the cleaned up version of this email post http://mail.python.org/pipermail/python-list/2003-May/162433.html .