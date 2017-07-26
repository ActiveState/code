import os
import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4.QtNetwork import *

__version__ = "0.1 20091002"
__appname__ = "minibrowser"

TITLE = "%s %s" % (__appname__, __version__)
HOMEPAGE = "http://example.com/"
HISTORY = os.path.join(os.path.dirname(sys.argv[0]), "%s.log" % (__appname__))

class BrowserWidget(QWidget):
    def __init__(self, datpath, parent=None):
        super(self.__class__, self).__init__(parent)
        self.browser = QWebView()
        self.lineedit = QLineEdit()
        
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setMargin(0)
        layout.addWidget(self.lineedit)
        layout.addWidget(self.browser)
        self.setLayout(layout)
        self.lineedit.setFocus()
        self.connect(self.lineedit, SIGNAL("returnPressed()"), self.entrytext)

        self.browser.load(QUrl(HOMEPAGE))
        self.browser.show()
        
    def entrytext(self):
        self.browser.load(QUrl(self.lineedit.text()))

class Window(QMainWindow):
    def __init__(self, histlogpath, parent=None):
        super(self.__class__, self).__init__(parent)
        self.browserWindow = BrowserWidget(histlogpath)
        self.setCentralWidget(self.browserWindow)
        self.setWindowTitle(TITLE)

        status = self.statusBar()
        status.setSizeGripEnabled(True)

        self.label = QLabel("")
        status.addWidget(self.label, 1)

        self.connect(self.browserWindow.browser, SIGNAL("loadFinished(bool)"), self.loadFinished)
        self.connect(self.browserWindow.browser, SIGNAL("loadProgress(int)"), self.loading)
        self.histlogpath = histlogpath

    def loadFinished(self, flag):
        """SLOT of load finished.
        """
        self.label.setText("Done")
        open(self.histlogpath, 'a').write(self.browserWindow.browser.url().toString() + "\n")

    def loading(self, percent):
        """SLOT of loading progress.
        """
        self.label.setText("Loading %d%%" % percent)
        self.browserWindow.lineedit.setText(self.browserWindow.browser.url().toString())

if __name__ == '__main__':
    QNetworkProxy.setApplicationProxy(QNetworkProxy(QNetworkProxy.HttpProxy, "proxy.example.com", 8080))
    app = QApplication(sys.argv)
    window = Window(HISTORY)
    window.show()
    app.exec_()
