#!/usr/bin/python

"""
QtBreadCrumbs - A simple BreadCrumbs Navigation Bar

###================ Program Info ================###
    Program Name : QtBreadCrumbs
    Version : 1.0.0
    Platform : Linux/Unix
    Requriements :
        Must :
            modules PyQt4
    Python Version : Python 2.6 or higher
    Author : Britanicus
    Email : marcusbritanicus@gmail.com
    License : GPL version 3
###==============================================###
"""

### =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #

	#
	# Copyright 2012 Britanicus <marcusbritanicus@gmail.com>
	#

	#
	# This program is free software; you can redistribute it and/or modify
	# it under the terms of the GNU General Public License as published by
	# the Free Software Foundation; either version 2 of the License, or
	# ( at your option ) any later version.
	#

	#
	# This program is distributed in the hope that it will be useful,
	# but WITHOUT ANY WARRANTY; without even the implied warranty of
	# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	# GNU General Public License for more details.
	#

	#
	# You should have received a copy of the GNU General Public License
	# along with this program; if not, write to the Free Software
	# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
	# MA 02110-1301, USA.
	#

### =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class QtBreadCrumbMenu( QLabel ) :
	"""QlLabel BreadCrumbMenu
	"""

	openThisLocation = pyqtSignal( "QString" )

	def __init__( self, path ) :
		"""Class initialiser
		"""

		QLabel.__init__( self )

		self.cwd = QDir( path )
		self.cwd.setFilter( QDir.NoDotAndDotDot | QDir.Dirs )

		self.setPixmap( QIcon.fromTheme( "arrow-right" ).pixmap( QSize( 16, 16 ) ) )
		self.menu = QMenu()
		self.menu.setStyleSheet( "menu-scrollable: 1;" )
		self.menu.aboutToHide.connect( self.onMenuHidden )

	def mousePressEvent( self, mEvent ) :
		"""Over riding the MousePress to show a menu
		"""

		self.menu.clear()
		if self.cwd.entryList().count() :
			for d in self.cwd.entryList() :
				action = self.menu.addAction( QIcon.fromTheme( "folder" ), d )
				action.triggered.connect( self.onMenuItemClicked )

		else :
			action = self.menu.addAction( "No folders" )
			action.setDisabled( True )

		if self.menu.isVisible() :
			self.setPixmap( QIcon.fromTheme( "arrow-right" ).pixmap( QSize( 16, 16 ) ) )
			self.menu.hide()

		else :
			self.setPixmap( QIcon.fromTheme( "arrow-down" ).pixmap( QSize( 16, 16 ) ) )
			self.menu.popup( self.mapToGlobal( self.frameRect().bottomLeft() ) )

		mEvent.accept()

	def onMenuHidden( self ) :
		"""onMenuHidden() -> None

		Reset the QLabel pixmap when the menu is hidden

		@return None
		"""

		self.setPixmap( QIcon.fromTheme( "arrow-right" ).pixmap( QSize( 16, 16 ) ) )

	def onMenuItemClicked( self ) :
		"""printAction() -> None

		Dummy to handle menu action click

		@return None
		"""

		self.openThisLocation.emit( self.cwd.filePath( self.sender().text() ) )

class QtBreadCrumb( QLabel ) :
	"""QLabel BreadCrumb
	"""

	openThisLocation = pyqtSignal(  "QString" )

	def __init__( self, path, current = False ) :
		"""Class initialiser
		"""

		QLabel.__init__( self )

		self.cwd = QDir( path )

		if self.cwd.isRoot() :
			self.setPixmap( QIcon.fromTheme( "drive-harddisk" ).pixmap( QSize( 16, 16 ) ) )

		elif self.cwd == QDir.home() :
			self.setPixmap( QIcon.fromTheme( "go-home" ).pixmap( QSize( 16, 16 ) ) )

		else :
			self.setText( self.cwd.dirName() )

		if current :
			self.setStyleSheet( "QLabel { font-weight: bold; }" )

	def mousePressEvent( self, mEvent ) :
		"""Over riding the MousePress to show a menu
		"""

		self.openThisLocation.emit( self.cwd.absolutePath() )
		mEvent.accept()

class QtBreadCrumbsBar( QWidget ) :
	"""QtBreadCrumbBar
	"""

	openLocation = pyqtSignal( "QString" )

	def __init__( self, address = QString( "/" ) ) :
		"""Class initialiser
		"""

		QWidget.__init__( self )

		self.cwd = QDir( address )
		self.createGui()

	def createGui( self ) :
		"""createGui() -> None

		Create a GUI

		@return None
		"""

		self.setContentsMargins( QMargins() )

		lyt = QHBoxLayout()
		lyt.setContentsMargins( QMargins() )
		self.setLayout( lyt )

		self.loadPath( self.cwd.absolutePath() )

	def loadPath( self, path ) :
		"""loadPath( QString ) -> None

		Load the path into the bar

		@return None
		"""

		self.cwd = QDir( path )

		if self.layout().count() :
			while self.layout().count() :
				wItem = self.layout().takeAt( 0 )
				wItem.widget().deleteLater()
				del wItem

			else :
				self.updateGeometry()
				self.adjustSize()

		f = QDir( path )
		while not f.isRoot() :
			crumb = QtBreadCrumb( QFileInfo( f.absolutePath() ).absolutePath() )
			crumb.openThisLocation.connect( self.handleCrumbAndMenuSignal )

			menu = QtBreadCrumbMenu( QFileInfo( f.absolutePath() ).absolutePath() )
			menu.openThisLocation.connect( self.handleCrumbAndMenuSignal )

			self.layout().insertWidget( 0, menu )
			self.layout().insertWidget( 0, crumb )

			f = QDir( QFileInfo( f.absolutePath() ).absolutePath() )

		else :
			menu = QtBreadCrumbMenu( self.cwd.absolutePath() )
			menu.openThisLocation.connect( self.handleCrumbAndMenuSignal )

			self.layout().addWidget( QtBreadCrumb( self.cwd.absolutePath(), True ) )
			self.layout().addWidget( menu )
			self.layout().addStretch()

	def handleCrumbAndMenuSignal( self, string ) :
		"""handleCrumbAndMenuSignal() -> None

		Handles QtBreadCrumbCrumb and QtBreadCrumbMenu Signals

		@return None
		"""

		self.loadPath( string )
		self.openLocation.emit( string )
