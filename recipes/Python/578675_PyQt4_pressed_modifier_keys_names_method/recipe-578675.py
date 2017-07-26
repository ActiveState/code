#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QApplication
import functools

modies = { 'shift': Qt.ShiftModifier,
           'control': Qt.ControlModifier,
           'alt': Qt.AltModifier,
           'meta': Qt.MetaModifier }

def check_modifiers(org_meth):
    """Add modifiers kwarg to a method that contains a tuple of currently pressed modifiers."""

    @functools.wraps(org_meth)
    def wrapper(*args, **kwargs):
        curr = QApplication.keyboardModifiers()
        kwargs['modifiers'] = tuple( name for name, which in modies.items() if curr & which == which )

        org_meth(*args, **kwargs)

    return wrapper


if __name__ == '__main__':

    import sip
    from PyQt4 import QtGui, QtCore

    class MainWindow(QtGui.QMainWindow):

        def __init__(self):
            super(MainWindow, self).__init__()


            centralWidget = QtGui.QWidget(self)
            layout = QtGui.QHBoxLayout(centralWidget)
            self.setCentralWidget(centralWidget)
            self.clickButton = QtGui.QPushButton("click", centralWidget)
            self.clickButton.clicked.connect(self.klick)
            layout.addWidget(self.clickButton)
            self.statusBar()
            self.setFixedWidth(600)

        @check_modifiers
        def klick(self, event, modifiers):
            ms = QtGui.QApplication.keyboardModifiers()
            m = "keyboardModifiers: {1:0=32b} {0} has been pressed"
            self.statusBar().showMessage(m.format(repr(modifiers), int(ms)))
            
    import sys
    app = QtGui.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
