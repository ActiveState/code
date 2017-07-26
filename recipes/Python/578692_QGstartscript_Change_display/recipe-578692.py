# -*- coding: utf-8; -*-

''' CoordsConf: Configure QGIS coordinate display
Store this script as .qgis2/python/startup.py

Redoute, 19.10.2013 '''

from __future__ import unicode_literals, division

import qgis
QgsPoint = qgis.core.QgsPoint
CoordinateReferenceSystem = qgis.core.QgsCoordinateReferenceSystem
CoordinateTransform = qgis.core.QgsCoordinateTransform
ProjectionSelector = qgis.gui.QgsProjectionSelector

import PyQt4
qActionsContextMenu = PyQt4.QtCore.Qt.ActionsContextMenu
qAlignCenter = PyQt4.QtCore.Qt.AlignCenter
qAlignHCenter = PyQt4.QtCore.Qt.AlignHCenter
qAlignRight = PyQt4.QtCore.Qt.AlignRight
qAlignVCenter = PyQt4.QtCore.Qt.AlignVCenter
qHorizontal = PyQt4.QtCore.Qt.Horizontal
qToolButtonTextOnly = PyQt4.QtCore.Qt.ToolButtonTextOnly
settings = PyQt4.QtCore.QSettings()
Action = PyQt4.QtGui.QAction
ButtonGroup = PyQt4.QtGui.QButtonGroup
Dialog = PyQt4.QtGui.QDialog
DialogButtonBox = PyQt4.QtGui.QDialogButtonBox
GroupBox = PyQt4.QtGui.QGroupBox
Label = PyQt4.QtGui.QLabel
LineEdit = PyQt4.QtGui.QLineEdit
msgBox = PyQt4.QtGui.QMessageBox.information
PushButton = PyQt4.QtGui.QPushButton
RadioButton = PyQt4.QtGui.QRadioButton
TabWidget = PyQt4.QtGui.QTabWidget
ToolButton = PyQt4.QtGui.QToolButton
VBoxLayout = PyQt4.QtGui.QVBoxLayout
Widget = PyQt4.QtGui.QWidget

class Config(object):
    # read Options
    dstAuthId = settings.value('CoordsConf/dstAuthId', 'EPSG:4326')
    dstCrs = CoordinateReferenceSystem(dstAuthId)
    rule1 = settings.value('CoordsConf/rule1', 0, type=int)
    rule2 = settings.value('CoordsConf/rule2', 0, type=int)
    rule3 = settings.value('CoordsConf/rule3', 0, type=int)
    rule4 = settings.value('CoordsConf/rule4', 0, type=int)

iface = qgis.utils.iface
mw = iface.mainWindow()
sb = mw.statusBar()
mc = iface.mapCanvas()
mr = mc.mapRenderer()

def makeGroup(parent, odict):
    l = VBoxLayout(parent)
    g = ButtonGroup(parent)
    for id, label in odict.iteritems():
        rb = RadioButton(label, parent)
        l.addWidget(rb)
        g.addButton(rb, id)
    return g

# actions of coord display
class Dlg(Dialog):
    def __init__(self):
        super(Dialog, self).__init__(mw)
        self.setWindowTitle('Configure Coords Display')
        layout = VBoxLayout(self)

        tabs = TabWidget(self)

        tabCrs = Widget()
        lTabCrs = VBoxLayout(tabCrs)

        self.ps = ProjectionSelector(tabCrs)
        self.ps.setSelectedAuthId(Config.dstAuthId)
        lTabCrs.addWidget(self.ps)

        tabs.addTab(tabCrs, '&CRS for coords display')

        tabOptions = Widget()
        lTabOptions = VBoxLayout(tabOptions)

        g1 = GroupBox('&1) When \'on the fly\' CRS transformation is enabled and active layer CRS is available:', tabOptions)
        self.o1 = makeGroup(g1,
            {0: 'Show display CRS',
             2: 'Show project CRS',
             3: 'Show active layer CRS',
             5: 'Show screen coords'})
        lTabOptions.addWidget(g1)

        g2 = GroupBox('&2) When \'on the fly\' CRS transformation is enabled and active layer CRS is not available:', tabOptions)
        self.o2 = makeGroup(g2,
            {0: 'Show display CRS',
             2: 'Show project CRS',
             5: 'Show screen coords'})
        lTabOptions.addWidget(g2)

        g3 = GroupBox('&3) When \'on the fly\' CRS transformation is disabled and active layer CRS is available:', tabOptions)
        self.o3 = makeGroup(g3,
            {1: 'Show display CRS, reprojected via active layer CRS',
             0: 'Show display CRS, reprojected via project CRS',
             4: 'Show active layer CRS',
             2: 'Show project CRS',
             5: 'Show screen Coords'})
        lTabOptions.addWidget(g3)

        g4 = GroupBox('&4) When \'on the fly\' CRS transformation is disabled and active layer CRS is not available:', tabOptions)
        self.o4 = makeGroup(g4,
            {0: 'Show display CRS, reprojected via project CRS',
             2: 'Show project CRS',
             5: 'Show screen Coords'})
        lTabOptions.addWidget(g4)

        lTabOptions.addStretch(1)
        tabs.addTab(tabOptions, '&Options')

        layout.addWidget(tabs)

        bbox = DialogButtonBox(self)
        bbox.setOrientation(qHorizontal)
        bbox.setStandardButtons(DialogButtonBox.Ok | DialogButtonBox.Cancel)
        bbox.accepted.connect(self.accept)
        bbox.rejected.connect(self.reject)
        layout.addWidget(bbox)
        self.adjustSize() ### ???

        self.ps.setSelectedAuthId(Config.dstAuthId)
        self.o1.button(Config.rule1).setChecked(True)
        self.o2.button(Config.rule2).setChecked(True)
        self.o3.button(Config.rule3).setChecked(True)
        self.o4.button(Config.rule4).setChecked(True)
dlg = Dlg()

def configure():
    if dlg.exec_():
        Config.dstAuthId = dlg.ps.selectedAuthId()
        Config.dstCrs = CoordinateReferenceSystem(Config.dstAuthId)
        settings.setValue('CoordsConf/dstAuthId', Config.dstAuthId)
        Config.rule1 = dlg.o1.checkedId()
        settings.setValue('CoordsConf/rule1', Config.rule1)
        Config.rule2 = dlg.o2.checkedId()
        settings.setValue('CoordsConf/rule2', Config.rule2)
        Config.rule3 = dlg.o3.checkedId()
        settings.setValue('CoordsConf/rule3', Config.rule3)
        Config.rule4 = dlg.o4.checkedId()
        settings.setValue('CoordsConf/rule4', Config.rule4)

# remove builtin statusbar widgetgs
# check extents view button (reduces calculations in QgisApp::showMouseCoordinate)
w = sb.findChild(object, 'mToggleExtentsViewButton')
w.setChecked(True)
sb.removeWidget(w)
sb.removeWidget(sb.findChild(object, 'mCoordsLabel'))
sb.removeWidget(sb.findChild(object, 'mCoordsEdit'))

# create new label widgets for statusbar
crsButton = ToolButton(sb)
crsButton.setToolButtonStyle(qToolButtonTextOnly)
crsButton.setMinimumWidth(20)
crsButton.setMaximumHeight(20)
crsButton.setAutoRaise(True)
crsButton.clicked.connect(configure)
sb.insertPermanentWidget(1, crsButton)

xyButton = ToolButton(sb)
xyButton.setToolButtonStyle(qToolButtonTextOnly)
xyButton.setMinimumWidth(200)
xyButton.setMaximumHeight(20)
xyButton.setAutoRaise(True)
sb.insertPermanentWidget(2, xyButton)

# bind signal
def showCoords(xy):
    # Which rule is applicable?
    c1 = mr.hasCrsTransformEnabled()
    l = iface.activeLayer()
    c2 = bool(l and l.crs())
    if c1 and c2:
        rule = Config.rule1
    elif c1:
        rule = Config.rule2
    elif c2:
        rule = Config.rule3
    else:
        rule = Config.rule4
    
    # transform xy and get auth id according to rule
    if rule == 0:
        xyCrs = mr.destinationCrs()
        xy = CoordinateTransform(xyCrs, Config.dstCrs).transform(xy)
        authId = Config.dstAuthId
    elif rule == 1:
        xyCrs = iface.activeLayer().crs()
        xy = CoordinateTransform(xyCrs, Config.dstCrs).transform(xy)
        authId = Config.dstAuthId
    elif rule == 2:
        authId = mr.destinationCrs().authid()
    elif rule == 3:
        xyCrs = mr.destinationCrs()
        layerCrs = iface.activeLayer().crs()
        xy = CoordinateTransform(xyCrs, layerCrs).transform(xy)
        authId = layerCrs.authid()
    elif rule == 4:
        authId = iface.activeLayer().crs().authid()
    elif rule == 5:
        xy = mc.mouseLastXY()
        xy = QgsPoint(xy.x(), xy.y())
        authId = 'Screen'

    # label buttons
    crsButton.setText(authId)
    xyButton.setText(xy.toString(5))

# init
showCoords(qgis.core.QgsPoint(0, 0))
mc.xyCoordinates.connect(showCoords)
