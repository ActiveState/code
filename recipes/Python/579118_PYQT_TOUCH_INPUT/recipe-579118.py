from PyQt4 import QtGui, QtCore
from decimal import Decimal

# applicationle widgets
SIP_WIDGETS = [QtGui.QLineEdit]

class MyFlatPushButton(QtGui.QPushButton):
    def __init__(self, caption, min_size=(50, 50)):
        self.MIN_SIZE = min_size
        QtGui.QPushButton.__init__(self, caption)
        self.setFocusPolicy(QtCore.Qt.NoFocus)

    def sizeHint(self):
        return QtCore.QSize(self.MIN_SIZE[0], self.MIN_SIZE[1])


class SoftInputWidget(QtGui.QDialog):
    def __init__(self, parent_object, keyboard_type='default'):
        QtGui.QDialog.__init__(self)
        self.setWindowFlags(QtCore.Qt.Tool | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.INPUT_WIDGET = None
        self.PARENT_OBJECT = parent_object
        self.signalMapper = QtCore.QSignalMapper(self)

        self.NO_ORD_KEY_LIST = list()
        self.NO_ORD_KEY_LIST.append(QtCore.Qt.Key_Left)
        self.NO_ORD_KEY_LIST.append(QtCore.Qt.Key_Up)
        self.NO_ORD_KEY_LIST.append(QtCore.Qt.Key_Right)
        self.NO_ORD_KEY_LIST.append(QtCore.Qt.Key_Down)
        self.NO_ORD_KEY_LIST.append(QtCore.Qt.Key_Backspace)
        self.NO_ORD_KEY_LIST.append(QtCore.Qt.Key_Enter)
        self.NO_ORD_KEY_LIST.append(QtCore.Qt.Key_Tab)
        self.NO_ORD_KEY_LIST.append(QtCore.Qt.Key_Escape)

        self.do_layout(keyboard_type)

        self.signalMapper.mapped[int].connect(self.buttonClicked)

    def do_layout(self, keyboard_type='default'):
        """
        @param   keyboard_type:
        @return:
        """
        gl = QtGui.QVBoxLayout()
        self.setFont(self.PARENT_OBJECT.font())
        number_widget_list = []
        sym_list = range(0, 10)
        for sym in sym_list:
            button = MyFlatPushButton(str(sym))
            button.KEY_CHAR = ord(str(sym))
            number_widget_list.append(button)

        button = MyFlatPushButton('*')
        button.KEY_CHAR = ord('*')
        number_widget_list.append(button)

        # alphabets
        alpha_widget_list = []
        sym_list    = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p',
                       'new_row',
                       'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l',
                       'new_row',
                       'z', 'x', 'c', 'v', 'b', 'n', 'm']
        for sym in sym_list:
            if sym == 'new_row':
                alpha_widget_list.append('new_row')
            else:
                button = MyFlatPushButton(sym)
                button.KEY_CHAR = ord(sym)
                alpha_widget_list.append(button)

        # back space
        control_widget_list = []
        button = MyFlatPushButton('<B')
        button.setToolTip('Backspace')
        button.KEY_CHAR = QtCore.Qt.Key_Backspace
        control_widget_list.append(button)
        control_widget_list.append('sep')

        # tab
        button = MyFlatPushButton('>T')
        button.KEY_CHAR = QtCore.Qt.Key_Tab
        control_widget_list.append(button)
        control_widget_list.append('sep')

        # space
        button = MyFlatPushButton('SPC')
        button.KEY_CHAR = QtCore.Qt.Key_Space
        control_widget_list.append(button)
        control_widget_list.append('sep')

        # close
        button = MyFlatPushButton('X')
        button.KEY_CHAR = QtCore.Qt.Key_Escape
        control_widget_list.append(button)
        control_widget_list.append('sep')

        # enter
        button = MyFlatPushButton('ENT', min_size=(110, 60))
        button.KEY_CHAR = QtCore.Qt.Key_Enter
        control_widget_list.append(button)
        control_widget_list.append('sep')

        alist = list()
        alist.append((QtCore.Qt.Key_Left,  'L-A'))
        alist.append((QtCore.Qt.Key_Right, 'R-A'))
        alist.append((QtCore.Qt.Key_Up,    'U-A'))
        alist.append((QtCore.Qt.Key_Down,  'D-A'))
        for key in alist:
            button = MyFlatPushButton(key[1])
            button.KEY_CHAR = key[0]
            control_widget_list.append(button)

        MAX_COL = 10
        col     = 0
        tlist   = list()
        if keyboard_type == 'numeric':
            widget_list = number_widget_list
        elif keyboard_type == 'alpha':
            widget_list = alpha_widget_list
        else:
            widget_list = list()
            widget_list.extend(number_widget_list)
            widget_list.append('new_row')
            widget_list.extend(alpha_widget_list)

        widget_list.append('new_row')
        widget_list.extend(control_widget_list)

        for widget in widget_list:
            if widget == 'new_row':
                col = MAX_COL
            elif widget == 'sep':
                tlist.append(self.get_vline())
                continue
            else:
                tlist.append(widget)
                widget.clicked.connect(self.signalMapper.map)
                self.signalMapper.setMapping(widget, widget.KEY_CHAR)

            if col == MAX_COL:
                col = 0
                v = QtGui.QHBoxLayout()
                v.addStretch()
                v.setSpacing(5)
                map(v.addWidget, tlist)
                v.addStretch()
                gl.addLayout(v)
                tlist = []
            else:
                col += 1

        v = QtGui.QHBoxLayout()
        v.setSpacing(5)
        v.addStretch()
        map(v.addWidget, tlist)
        v.addStretch()
        gl.addLayout(v)
        gl.setContentsMargins(0, 0, 0, 0)
        gl.setSpacing(5)
        gl.setSizeConstraint(gl.SetFixedSize)

        self.setLayout(gl)

    def reject(self):
        self.buttonClicked(QtCore.Qt.Key_Escape)

    def buttonClicked(self, char_ord):
        w = self.INPUT_WIDGET
        if char_ord in self.NO_ORD_KEY_LIST:
            keyPress = QtGui.QKeyEvent(QtCore.QEvent.KeyPress, char_ord, QtCore.Qt.NoModifier, '')
        else:
            keyPress = QtGui.QKeyEvent(QtCore.QEvent.KeyPress, char_ord, QtCore.Qt.NoModifier, chr(char_ord))

        # send keypress event to widget
        QtGui.QApplication.sendEvent(w, keyPress)

        # line edit returnPressed event is triggering twise for press and release both
        # that is why do not send release event for special key
        if char_ord not in self.NO_ORD_KEY_LIST:
            keyRelease = QtGui.QKeyEvent(QtCore.QEvent.KeyPress, char_ord, QtCore.Qt.NoModifier, '')
            QtGui.QApplication.sendEvent(w, keyRelease)

        # hide on enter or esc button click
        if char_ord in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Escape):
            self.hide()

    def show_input_panel(self, widget):
        self.INPUT_WIDGET = widget
        self.show()
        self.update_panel_position()

    def update_panel_position(self):
        widget = self.INPUT_WIDGET
        if not widget: return

        widget_rect         = widget.rect()
        widget_bottom       = widget.mapToGlobal(QtCore.QPoint(widget.frameGeometry().x(), widget.frameGeometry().y())).y()
        screen_height       = QtGui.qApp.desktop().availableGeometry().height()
        input_panel_height  = self.geometry().height() + 5

        if (screen_height - widget_bottom) > input_panel_height:
            # display input panel at bottom of widget
            panelPos = QtCore.QPoint(widget_rect.left(), widget_rect.bottom() + 2)
        else:
            # display input panel at top of widget
            panelPos = QtCore.QPoint(widget_rect.left(), widget_rect.top() - input_panel_height)

        panelPos = widget.mapToGlobal(panelPos)
        self.move(panelPos)

    def _get_line(self, vertical=True):
        line = QtGui.QFrame()
        line.setContentsMargins(0, 0, 0, 0)
        if vertical is True:
            line.setFrameShape(line.VLine)
        else:
            line.setFrameShape(line.HLine)
        line.setFrameShadow(line.Sunken)
        return line

    def get_hline(self):
        return self._get_line(vertical=False)

    def get_vline(self):
        return self._get_line()


class TouchInterface(QtCore.QObject):
    def __init__(self, PARENT_WIDGET):
        QtCore.QObject.__init__(self)
        self._PARENT_WIDGET        = PARENT_WIDGET
        self._input_panel_all      = SoftInputWidget(PARENT_WIDGET, 'default')
        self._input_panel_numeric  = SoftInputWidget(PARENT_WIDGET, 'numeric')

    def childEvent(self, event):
        if event.type() == QtCore.QEvent.ChildAdded:
            if isinstance(event.child(), *SIP_WIDGETS):
                event.child().installEventFilter(self)

    def eventFilter(self, widget, event):
        if self._PARENT_WIDGET.focusWidget() == widget and event.type() == QtCore.QEvent.MouseButtonPress:
            if hasattr(widget, 'keyboard_type'):
                if widget.keyboard_type == 'default':
                    self._input_panel_all.show_input_panel(widget)
                elif widget.keyboard_type == 'numeric':
                    self._input_panel_numeric.show_input_panel(widget)

        return False


class TouchInputWidget(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.touch_interface = TouchInterface(self)

    def childEvent(self, event):
        self.touch_interface.childEvent(event)

    def eventFilter(self, widget, event):
        return self.touch_interface.eventFilter(widget, event)


class ExampleWidget(TouchInputWidget):
    def __init__(self):
        TouchInputWidget.__init__(self)

        self.txtNumeric    = QtGui.QLineEdit()
        # actiate touch input
        self.txtNumeric.keyboard_type = 'numeric'

        self.txtText = QtGui.QLineEdit()
        # activate touch input
        self.txtText.keyboard_type = 'default'

        gl = QtGui.QVBoxLayout()
        gl.addWidget(self.txtNumeric)
        gl.addWidget(self.txtText)

        self.setWindowTitle('Touch Input Demo')
        self.setLayout(gl)

if __name__ == '__main__':
    app = QtGui.QApplication([])
    ExampleWidget().show()
    app.exec_()
