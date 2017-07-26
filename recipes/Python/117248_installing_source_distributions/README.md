## installing source distributions on windows

Originally published: 2002-03-19 03:11:37
Last updated: 2002-04-10 20:04:47
Author: Thomas Heller

Distutil's bdist_wininst installers offer uninstallation support for Python extensions, many developers however only distribute sources in zip or tar.gz format. The typical steps to install such a distribution are:\n- download the file\n- unpack with winzip into a temporary directory\n- open a command prompt and type 'python setup.py install'\n- remove the temporary directory\n\nThis script unpacks a source distribution into a temporary directory, builds a windows installer on the fly, executes it, and cleans everything up afterward.