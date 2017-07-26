## DistCC 'top'

Originally published: 2011-10-31 18:26:44
Last updated: 2013-12-01 11:19:56
Author: Mike 'Fuzzy' Partin

A small recipe for a curses based, 'top'-like monitor for DistCC. I know there is already distccmon-text, but I don't like it, and much prefer this sytle of monitoring. Note that I don't keep hosts around in the list like distccmon-gui/gnome. The screen is drawn for exactly what is currently in state. The terminal size is respected at initialization time, however resize events aren't handled. There is color designation of job types.