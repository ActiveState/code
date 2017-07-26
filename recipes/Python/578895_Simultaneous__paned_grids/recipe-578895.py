# Version 0.1
# Author: Miguel Martinez Lopez
# Uncomment the next line to see my email
# print "Email: ", "61706c69636163696f6e616d656469646140676d61696c2e636f6d".decode("hex")


from Tkinter import *
from collections import defaultdict
import itertools


class connected_Panedgrids(object):

	def __init__(self, numRows=0, numColumns=0):
		if type(numRows) is not int:
			raise Exception("The number of shared rows is not an int.")

		if type(numColumns) is not int:
			raise Exception("The number of shared columns is not an int.")

		self.numberOfSharedRows = numRows
		self.numberOfSharedColumns = numColumns

		self.panedwindow_conexion = SimultaneousPanels()

		self.__connected_widgets = {}

	def create_widget(self, master, shared_rows=[], shared_columns=[], shared_panedwindows=[], **kwargs):
		panedgrid_widget = PanedGrid(master, **kwargs)

		self.add_widget(panedgrid_widget, shared_rows, shared_columns, shared_panedwindows)
		return panedgrid_widget

	def add_widget(self, panedgrid_widget, shared_rows=[], shared_columns=[], shared_panedwindows=[]):

		if shared_rows == 'all':
			shared_rows = range(self.numberOfSharedRows)

		if shared_columns == 'all':
			shared_columns = range(self.numberOfSharedColumns)

		widget_bundle = {	'panedgrid_widget': panedgrid_widget,
							'shared_rows' : shared_rows,
							'shared_columns': shared_columns,
							'shared_panedwindows': shared_panedwindows
						}

		self.__connected_widgets[str(panedgrid_widget)] = widget_bundle

	def delete_widget(self, widget_reference):
		del self.__connected_widgets[str(panedgrid_widget)]

	def update(self):
		self.panedwindow_conexion.clear()

		height_list = [0]*self.numberOfSharedRows
		width_list = [0]*self.numberOfSharedColumns

		for bundle_INFO in self.__connected_widgets.values():
			panedgrid_widget = bundle_INFO['panedgrid_widget']
			shared_panedwindows = bundle_INFO['shared_panedwindows']
			shared_rows = bundle_INFO['shared_rows']
			shared_columns = bundle_INFO['shared_columns']

			if not panedgrid_widget.builded:
				panedgrid_widget.build()


			if shared_panedwindows == 'all':
				shared_panedwindows = range(len(panedgrid_widget.panedwindows))

			for conexion_index, panedwindow_index in enumerate(shared_panedwindows):
				internal_panedwindow = panedgrid_widget.panedwindows[panedwindow_index]
				self.panedwindow_conexion.add_widget(internal_panedwindow, tag=conexion_index)

				pane_indices = range(*internal_panedwindow.index_range)

				if panedgrid_widget.orient == HORIZONTAL:
					shared_columns.extend(pane_indices)
				else:
					shared_rows.extend(pane_indices)


			shared_rows = sorted(set(shared_rows))
			shared_columns = sorted(set(shared_columns))

			if self.numberOfSharedRows != len(shared_rows):
				raise Exception("The number of shared rows %s is not equal to %s." % (len(shared_rows), self.numberOfSharedRows) )
			if self.numberOfSharedColumns != len(shared_columns):
				raise Exception("The number of shared columns %s is not equal to %s." % (len(shared_columns), self.numberOfSharedColumns) )

			bundle_INFO['shared_rows'] = shared_rows
			bundle_INFO['shared_columns'] = shared_columns

			for position_in_height_list, row_index in enumerate(shared_rows):
				height_list[position_in_height_list] = max(
												height_list[position_in_height_list],
												panedgrid_widget.get_row_height( row_index )
												)


			for position_in_width_list, column_index in enumerate(shared_columns):
				width_list[position_in_width_list] = max(
												width_list[position_in_width_list],
												panedgrid_widget.get_column_width( column_index )
												)

		for bundle_INFO in self.__connected_widgets.values():

			for positionInList, rowIndex in enumerate(bundle_INFO['shared_rows']):
				bundle_INFO['panedgrid_widget'].rowconfigure(rowIndex, height = height_list[positionInList])

			for positionInList, columnIndex in enumerate(bundle_INFO['shared_columns']):
				bundle_INFO['panedgrid_widget'].columnconfigure(columnIndex, width = width_list[positionInList])



class SimultaneousPanels(PanedWindow):

 	def __init__(self):
		self.collectionOfPanedWindows = {}

	def create_widget(self,master, tag= '_default', **kargs):
		widget = PanedWindow(master, **kargs)
		self.add_widget(widget,tag)

		return widget

	def add_widget(self, widget, tag):
		widget.other_paned_windows = []

		if tag in self.collectionOfPanedWindows:
			for pwindow in self.collectionOfPanedWindows[tag]:
				widget.other_paned_windows.append(pwindow)
				pwindow.other_paned_windows.append(widget)

			self.collectionOfPanedWindows[tag].append(widget)
		else:
			self.collectionOfPanedWindows[tag] = [widget]

		widget.bindtags( ('SimultaneousPanels',)+ widget.bindtags() )
		widget.bind_class('SimultaneousPanels', '<Button-1>', self.sash_mark)
		widget.bind_class('SimultaneousPanels', '<B1-Motion>', self.sash_dragto)

	def sash_mark(self,event):
		this_widget = event.widget

		identity = this_widget.identify(event.x, event.y)

		if len(identity) ==2:
			index = identity[0]
			this_widget.activedSash=index
		else:
			this_widget.activedSash = None

	def sash_dragto(self,event):
		this_widget = event.widget
		activedSash = this_widget.activedSash

		if activedSash != None:
			for pwindow in this_widget.other_paned_windows:
				pwindow.sash_place(activedSash, event.x, event.y)

	def clear(self):
		for list_of_panels in self.collectionOfPanedWindows.values():
			for panel in list_of_panels:
				del panel.other_paned_windows
				self.delete_bindtag(panel)
		self.collectionOfPanedWindows = {}

	def delete_tag(self, tag):
		for widget in self.collectionOfPanedWindows[tag]:
			del widget.other_paned_windows
			self.delete_bindtag(widget)

		del self.collectionOfPanedWindows[tag]

	def delete_widget(self, widget, tag):
		for panel in self.collectionOfPanedWindows[tag]:
			panel.other_paned_windows.remove(widget)
		self.delete_bindtag(widget)
		del widget.other_paned_windows

	def delete_bindtag(self, widget):
		new_bindtags = list(widget.bindtags())
		new_bindtags.remove('SimultaneousPanels')
		widget.bindtags(tuple(new_bindtags))

		
class PanedGrid(Frame):
	def __init__(self, master, orient=HORIZONTAL, minsize=20, columnWidths = {}, rowHeights={}, fixedPanes = []):
		Frame.__init__(self,master)

		if orient in (HORIZONTAL, VERTICAL):
			self.orient = orient
		else:
			raise Exception("orient must be 'horizontal' or 'vertical, not '%s'." % orient)

		if type(minsize) is int:
			self.minsize = minsize
		else:
			raise Exception("Minsize must be an integer.")

		self.fixedPanes = set(fixedPanes)

		self.__packSideBetweenPanes = LEFT if self.orient == HORIZONTAL else TOP
		self.__packSideInsidePane = TOP if self.orient == HORIZONTAL else LEFT
		self.__cellFill = X if self.orient == HORIZONTAL else Y

		self.userDefinedWidths = columnWidths
		self.userDefinedHeights = rowHeights

		self.__panes = {}

		self.builded = False

		self.clear_table()


	def clear_table(self):
		if not self.builded:
			self.__gridOfWidgets = {}

			self.__rows = defaultdict(set)
			self.__columns = defaultdict(set)

			self.__rowHeights = {}
			self.__columnWidths = {}

			self.userDefinedWidths = {}
			self.userDefinedHeights = {}

		else:
			raise Exception("You can't clear the table one this is builded.")

	def rowIndices(self):
		return self.__rows.keys()

	def columnIndices(self):
		return self.__columns.keys()

	def numberOfRows(self):
		return len(self.__rows)

	def numberOfColumns(self):
		return len(self.__columns)

	def update_cell(self, coordinates, widget):
		if not self.builded:
			raise Exception("First you must to build the panedgrid.")

		if coordinates in self.__gridOfWidgets:
			master = self.__gridOfWidgets[coordinates].pack_info()['in']
			self.__gridOfWidgets[coordinates].destroy()
			self.__gridOfWidgets[coordinates] = widget
			widget.pack(in_=master, expand=YES, fill=BOTH)
		else:
			raise Exception("There is no widget with coordiantes: %s." % coordinates)


	def build(self):
		if self.builded:
			raise Exception("You have just builded the grid before.")

		if not self.__gridOfWidgets: return

		if self.calculate_dimensions:
			self.__calculate_list_of_cell_widths_and_heights()

		self.panedwindows = []

		listOfCellCoordinates = list(itertools.product(self.__rows, self.__columns))

		if self.orient == HORIZONTAL:
			listOfCellCoordinates.sort(key = lambda item: (item[1], item[0]))
		else:
			listOfCellCoordinates.sort()

		# We set up the first pane index
		pane_index = self.__columns[0] if self.orient == HORIZONTAL else self.__rows[0]

		position_of_main_index = 1 if self.orient == HORIZONTAL else 0

		newPanedWindow = True

		for cell_coordinates in listOfCellCoordinates:

			main_index = cell_coordinates[position_of_main_index]
			if pane_index != main_index:
				# Creating a new pane
				pane_index = main_index

				if pane_index in self.fixedPanes:
					frameOfPane = Frame(self)
					frameOfPane.pack(side=self.__packSideBetweenPanes)
					newPanedWindow = True
				else:
					if newPanedWindow:
						paneMaster = PanedWindow(self,orient=self.orient, bd=0, sashwidth=3)
						paneMaster.index_range = (pane_index, pane_index + 1 )

						paneMaster.pack(side=self.__packSideBetweenPanes)

						self.panedwindows.append(paneMaster)
						newPanedWindow = False
					else:
						beginning_of_range = paneMaster.index_range[0]
						ending_of_range = pane_index + 1
						paneMaster.index_range = (beginning_of_range, ending_of_range)

					frameOfPane = Frame(paneMaster)
					frameOfPane.pack()
					paneMaster.add(frameOfPane)

					paneMaster.paneconfigure(frameOfPane, minsize=self.minsize)

				sizeOfPane = self.__columnWidths[pane_index] if self.orient == HORIZONTAL else self.__rowHeights[pane_index]

				if self.orient == HORIZONTAL:
					frameOfPane.configure(width=sizeOfPane, height=self.tableHeight)
				else:
					frameOfPane.configure(width=self.tableWidth, height=sizeOfPane)

				frameOfPane.pack_propagate(False)

				self.__panes[pane_index] = frameOfPane

			cellFrame = Frame(frameOfPane, bd=1, relief=SUNKEN)
			cellFrame.pack(side=self.__packSideInsidePane, expand=YES, fill=self.__cellFill)
			cellFrame.pack_propagate(False)

			widget = self.__gridOfWidgets[cell_coordinates]

			if widget:
				widget.lift()
				widget.pack(in_=cellFrame, expand=YES, fill=BOTH)

				if self.orient == HORIZONTAL:
					cellFrame.configure( height=self.__rowHeights[ cell_coordinates[0] ] )
				else:
					cellFrame.configure( width=self.__columnWidths[ cell_coordinates[1] ] )

		self.builded = True

	def __calculate_list_of_cell_widths_and_heights(self):
		self.__rowHeights = self.userDefinedHeights.copy()
		self.__columnWidths = self.userDefinedWidths.copy()

		for coordinate, widget in self.__gridOfWidgets.items():
			i , j = coordinate
			if i not in self.userDefinedHeights:
				self.__rowHeights[i] = max(self.__rowHeights.get(i,0),widget.winfo_reqheight())

			if j not in self.userDefinedWidths:
				self.__columnWidths[j] = max(self.__columnWidths.get(j,0),widget.winfo_reqwidth())

		self.calculate_dimensions = False

	@property
	def tableHeight(self):
		return sum(self.__rowHeights.values())

	@property
	def tableWidth(self):
		return sum(self.__columnWidths.values())


	def rowconfigure(self,row, height=None, fixed = None):
		if row not in self.__rows:
			raise Exception("Row %d doesn't exists." % column)

		if height is not None:

			if type(height) is not int: raise Exception("The height must be an integer:%s"%height)

			self.userDefinedHeights[row] = height

			if self.orient == VERTICAL:
				self.__panes[row].configure(height=height)
			else:
				for column in self.__rows[row]:
					cellFrame = self.__gridOfWidgets[row,column].pack_info()['in']
					cellFrame.configure(height=height)

		if fixed is not None:
			if self.orient == HORIZONTAL:
				raise Exception("You can't set fixed property on a row because 'orient' is VERTICAL.")

			self.fix_pane(index, fixed)

	def columnconfigure(self,column, width=None, fixed = None):
		if column not in self.__columns:
			raise Exception("Column %d doesn't exists." % column)

		if width is not None:
			if type(width) is not int: raise Exception("The width must be an integer:%s"%width)

			self.userDefinedWidths[column] = width

			if self.orient == HORIZONTAL:
				self.__panes[column].configure(width=width)
			else:
				for row in self.__columns[column]:
					cellFrame = self.__gridOfWidgets[row,column].pack_info()['in']
					cellFrame.configure(width=width)

		if fixed is not None:
			if self.orient == VERTICAL:
				raise Exception("You can't set fixed property on a column because 'orient' is HORIZONTAL.")

			self.fix_pane(index, fixed)

	def fix_pane(index, fixed=True):
		if self.builded:
			raise Exception("You can't modify the fixed of the panes once you builded the grid.")

		if fixed == True:
			self.fixedPanes.add(index)
		elif fixed == False:
			self.fixedPanes.discard(index)
		else:
			raise Exception("fixed must be 'True' or 'False'.")

	def fix_all_panes(self):
		if self.builded:
			raise Exception("You can't modify the fixed of the panes once you builded the grid.")

		fixedPanes_list = self.__columns.keys() if self.orient == HORIZONTAL else self.__rows.keys()
		self.fixedPanes = set(fixedPanes_list)

	def realease_all_panes(self):
		if self.builded:
			raise Exception("You can't modify the fixed of the panes once you builded the grid.")

		self.fixedPanes = set()

	def is_a_fixed_pane(self, index ):
		paneWidget = self.__panes[index]

		parent = self.nametowidget( paneWidgetid.winfo_parent() )

		if parent.__class__.name == 'PanedWindow':
			return True
		else:
			return False

	def get_row_height(self, row):
		if self.calculate_dimensions:
			self.__calculate_list_of_cell_widths_and_heights()

		if self.orient == HORIZONTAL:
			if self.builded:
				return self.__panes[row].winfo_height()
			else:
				return self.__rowHeights[row]
		else:
			return self.__rowHeights[row]

	def get_column_width(self, column):
		if self.calculate_dimensions:
			self.__calculate_list_of_cell_widths_and_heights()

		if self.orient == HORIZONTAL:
			return self.__columnWidths[column]
		else:
			if self.builded:
				return self.__panes[column].winfo_width()
			else:
				return self.__columnWidths[column]

	def check_coordinates(self, coordinates):
		if type(coordinates) is int:
			i = 0
			j = coordinates
 		else:
			try:
				i, j = coordinates
				if type(i) is not int or type(j) is not int:
					raise Exception("Invalid coordinate")
			except:
				raise Exception("Invalid coordinate")

		return (i,j)

	def __getitem__(self, coordinates):
		coordinates = self.check_coordinates(coordinates)

		return self.__gridOfWidgets.get(coordinates)


	def __setitem__(self,coordinates, widget):
		if self.builded:
			raise Exception("The panedgrid was builded. Use cell_update() instead.")

		i , j = self.check_coordinates(coordinates)

		self.__gridOfWidgets[i,j] = widget

		self.__rows[i].add(j)
		self.__columns[j].add(i)

		self.calculate_dimensions = True

	def __delitem__(self, coordinates ):
		if self.builded:
			raise Exception("The panedgrid was builded. Use cell_update() instead.")

		i, j = self.check_coordinates(coordinates)

		del self.__gridOfWidgets[i,j]

		self.__rows[i].discard(j)
		if not self.__rows[i]: del self.__rows[i]

		self.__columns[j].discard(i)
		if not self.__columns[j]: del self.__columns[j]

		self.calculate_dimensions = True

	def grid(self, *args, **kargs):
		if not self.builded: self.build()
		Frame.grid(self,*args, **kargs)

	def pack(self, *args, **kargs):
		if not self.builded: self.build()
		Frame.pack(self,*args, **kargs)


				
				
def test():
	import random

	root = Tk()

	def table_of_random_widgets(master, numRows,numColumns, **kwargs):
		import ttk

		demo = testConnection.create_widget(master, shared_columns ='all', shared_panedwindows='all', **kwargs)

		tkinterWidgets =  (
					(Label, {'text':'This is a label'}),
					(Label, {'text':'This is another label', 'bg':'yellow'}),
					(Checkbutton,{}),
					(Button, {'text':'Click me'}),
					(ttk.Combobox, {'values':('item1', 'item2','item3','item4')})
					)

		for i in range(numRows):
			for j in range(numColumns):
				widgetClass, args = random.choice(tkinterWidgets)
				widget = widgetClass(demo,**args)

				demo[i,j] =  widget

		return demo
	testConnection = connected_Panedgrids(0,6)

	table1 = table_of_random_widgets(root, numRows=4,numColumns=6, fixedPanes=[2,5])
	table2 = table_of_random_widgets(root, numRows=4,numColumns=6, fixedPanes=[2,5])

	testConnection.update()

	Label(root, text= "Two different paned grids connected. Columns 2 and 5 are fixed.").pack(anchor=NW,pady=7, padx=12)
	table1.pack(anchor=NW,pady=2, padx=12)

	emptySpace = Frame(root, height =50)
	emptySpace.pack()

	table2.pack(anchor=NW,pady=2, padx=12)

	emptySpace = Frame(root, height =20)
	emptySpace.pack()


	root.mainloop()


if __name__ == '__main__':
	test()
