from Cocoa import NSTextView, NSMakeRect
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class WindowWidget(QWidget):
    def __init__(self, parent=None):
        super(WindowWidget, self).__init__(parent)
        cv = QMacCocoaViewContainer(0, self)
        cv.move(100, 100)
        cv.resize(300, 300)
        tv = NSTextView.alloc().initWithFrame_(NSMakeRect(0, 0, 300, 300))
        cv.setCocoaView(tv.__c_void_p__().value)

def main():
    import sys
    app = QApplication(sys.argv)
    w = WindowWidget()
    w.show()
    w.raise_()
    app.exec_()

if __name__ == '__main__':
    main()
