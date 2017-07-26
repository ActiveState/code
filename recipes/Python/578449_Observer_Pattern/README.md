## Observer Pattern

Originally published: 2013-02-04 20:55:10
Last updated: 2013-02-04 20:55:10
Author: Ilya Pashchenko

This is a Python implementation of the observer pattern described by Gamma et. al. It defines a one-to many dependency between objects so that when one object changes state, all its dependents are notified and updated automatically.\n\nThe example should output:\nSetting Data 1 = 10\nDecimalViewer: Subject Data 1 has data 10\nHexViewer: Subject Data 1 has data 0xa\nSetting Data 2 = 15\nHexViewer: Subject Data 2 has data 0xf\nDecimalViewer: Subject Data 2 has data 15\nSetting Data 1 = 3\nDecimalViewer: Subject Data 1 has data 3\nHexViewer: Subject Data 1 has data 0x3\nSetting Data 2 = 5\nHexViewer: Subject Data 2 has data 0x5\nDecimalViewer: Subject Data 2 has data 5\nDetach HexViewer from data1 and data2.\nSetting Data 1 = 10\nDecimalViewer: Subject Data 1 has data 10\nSetting Data 2 = 15\nDecimalViewer: Subject Data 2 has data 15