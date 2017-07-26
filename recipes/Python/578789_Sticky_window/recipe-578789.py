from PyQt4 import QtGui
from PyQt4.QtGui import QApplication
import sys, ctypes
class WINDOWPOS(ctypes.Structure):
    _fields_ = [
        ('hwnd', ctypes.c_ulong),
        ('hwndInsertAfter', ctypes.c_ulong),
        ('x', ctypes.c_int),
        ('y', ctypes.c_int),
        ('cx', ctypes.c_int),
        ('cy', ctypes.c_int),
        ('flags', ctypes.c_ulong)
    ]
    
WM_WINDOWPOSCHANGING = 0x46 #Sent to a window whose size, position, or place in the Z order is about to change

class AuMainWindow(QtGui.QMainWindow):
    def winEvent(self, message):
        if message.message == WM_WINDOWPOSCHANGING:
            stickAt = 10 #px near screen edge
            pos = WINDOWPOS.from_address(message.lParam)
            mon = QApplication.desktop().availableGeometry(self)
            if abs(pos.x - mon.left()) <= stickAt:
                pos.x = mon.left()
            elif abs(pos.x + pos.cx - mon.right()) <= stickAt:
                pos.x = mon.right() - pos.cx
            if abs(pos.y - mon.top()) <= stickAt:
                pos.y = mon.top()
            elif abs(pos.y + pos.cy - mon.bottom()) <= stickAt:
                pos.y = mon.bottom() - pos.cy
        return False, 0 
                
app = QtGui.QApplication(sys.argv)
mainwnd = AuMainWindow()
mainwnd.show()
sys.exit(app.exec_())
