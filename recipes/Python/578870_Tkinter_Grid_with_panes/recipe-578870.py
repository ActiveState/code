# Version 1.1
# Author: Miguel Martinez Lopez
# Uncomment the next line to see my email
# print "Email: ", "61706c69636163696f6e616d656469646140676d61696c2e636f6d".decode("hex")


from __future__ import print_function

from collections import defaultdict
import itertools


try:
    from tkinter import *
except ImportError:
    from Tkinter import *



class GridWithPanes(Frame):
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

        self.is_builded = False

        self.clear_table()

        self.is_displayed = False

    def clear_table(self):
        if not self.is_builded:
            self.__gridOfWidgets = {}

            self.__rows = defaultdict(set)
            self.__columns = defaultdict(set)

            self.__rowHeights = {}
            self.__columnWidths = {}

            self.userDefinedWidths = {}
            self.userDefinedHeights = {}
            
            self.calculate_dimensions = True
            
        else:
            raise Exception("You can't clear the table one this is is_builded.")

    @property
    def rowIndices(self):
        return self.__rows.keys()

    @property
    def columnIndices(self):
        return self.__columns.keys()

    @property
    def numberOfRows(self):
        return len(self.__rows)

    @property
    def numberOfColumns(self):
        return len(self.__columns)

    def update_cell(self, coordinates, widget):
        if not self.is_builded:
            raise Exception("First you must to build the GridWithPanes.")

        if coordinates in self.__gridOfWidgets:
            master = self.__gridOfWidgets[coordinates].pack_info()['in']
            self.__gridOfWidgets[coordinates].destroy()
            self.__gridOfWidgets[coordinates] = widget
            widget.pack(in_=master, expand=YES, fill=BOTH)
        else:
            raise Exception("There is no widget with coordiantes: %s." % coordinates)


    def build(self):
        if self.is_builded:
            raise Exception("You have just is_builded the grid before.")

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

        self.is_builded = True

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
        if self.calculate_dimensions:
            self.__calculate_list_of_cell_widths_and_heights()
            
        return sum(self.__rowHeights.values())

    @property
    def tableWidth(self):
        if self.calculate_dimensions:
            self.__calculate_list_of_cell_widths_and_heights()
        return sum(self.__columnWidths.values())


    def rowconfigure(self,row, height=None, fixed = None):
        if type(row) is str: row = int(row)
        
        if row not in self.__rows:
            raise Exception("Row %d doesn't exists." % row)

        if fixed is not None:
            if self.orient == HORIZONTAL:
                raise Exception("You can't set fixed property on a row because 'orient' is VERTICAL.")

            self.fix_pane(index, fixed)
            
        if height is not None:

            if type(height) is not int: raise Exception("The height must be an integer:%s"%height)

            self.userDefinedHeights[row] = height
            self.__rowHeights[row] = height
            self.calculate_dimensions = True
            
            if self.is_builded:
                if self.orient == VERTICAL:
                    if self.is_a_fixed_pane(row):
                        self.__panes[row].configure(height=height)
                    else:
                        self.__set_mobile_pane_size(row, height)
                else:
                    for column in self.__rows[row]:
                        cellFrame = self.__gridOfWidgets[row,column].pack_info()['in']
                        cellFrame.configure(height=height)


    def columnconfigure(self,column, width=None, fixed = None):
        if type(column) is str: column = int(column)
        
        if column not in self.__columns:
            raise Exception("Column %d doesn't exists." % column)

        if fixed is not None:
            if self.orient == VERTICAL:
                raise Exception("You can't set fixed property on a column because 'orient' is HORIZONTAL.")

            self.fix_pane(index, fixed)
                    
        if width is not None:
            if type(width) is not int: raise Exception("The width must be an integer:%s"%width)

            self.userDefinedWidths[column] = width
            self.__columnWidths[column] = width
            self.calculate_dimensions = True
            
            if self.is_builded:
                if self.orient == HORIZONTAL:
                    if self.is_a_fixed_pane(column):
                        self.__panes[column].configure(width=width)
                    else:
                        self.__set_mobile_pane_size(column, width)
                else:
                    for row in self.__columns[column]:
                        cellFrame = self.__gridOfWidgets[row,column].pack_info()['in']
                        cellFrame.configure(width=width)


    def fix_pane(index, fixed=True):
        if self.is_builded:
            raise Exception("You can't modify the fixed of the panes once you is_builded the grid.")

        if fixed == True:
            self.fixedPanes.add(index)
        elif fixed == False:
            self.fixedPanes.discard(index)
        else:
            raise Exception("fixed must be 'True' or 'False'.")

    def fix_all_panes(self):
        if self.is_builded:
            raise Exception("You can't modify the fixed of the panes once you is_builded the grid.")

        fixedPanes_list = self.__columns.keys() if self.orient == HORIZONTAL else self.__rows.keys()
        self.fixedPanes = set(fixedPanes_list)

    def realease_all_panes(self):
        if self.is_builded:
            raise Exception("You can't modify the fixed of the panes once you is_builded the grid.")

        self.fixedPanes = set()

    def is_a_fixed_pane(self, index ):
        paneWidget = self.__panes[index]

        parent = self.nametowidget( paneWidget.winfo_parent() )

        if parent.winfo_class() == 'Panedwindow':
            return False
        else:
            return True

    def __get_panedwindow_INFO(self, index):
        panedwindow = self.nametowidget( self.__panes[index].winfo_parent() )
        panedwindow_index = index - panedwindow.index_range[0]
        return panedwindow, panedwindow_index
                
    def __set_mobile_pane_size(self, index, size):
        panedwindow, panedwindow_index = self.__get_panedwindow_INFO(index)
        self.__set_pane_size_in_panedwindow(panedwindow, panedwindow_index, size)

    def __get_mobile_pane_size(self, index):
        panedwindow, panedwindow_index = self.__get_panedwindow_INFO(index)
        return self.__get_pane_size_in_panedwindow(panedwindow, panedwindow_index)

    def __set_pane_size_in_panedwindow(self,panedwindow, index, size):
        sash_coordinates = [0,0]
        last_index = len(panedwindow.panes()) - 1 
        
        if panedwindow['orient'] == HORIZONTAL:
            # Coordinate X
            position_coord = 0
                
            method_for_size_info = 'winfo_reqwidth'
        else:
            # Coordinate Y
            position_coord = 1
                
            method_for_size_info = 'winfo_reqheight'
                    
                    
        if index == 0:
            sash_index = 0            
            new_position = size            
        elif index == last_index:
            sash_index = last_index - 1
            new_position = getattr(panedwindow, method_for_size_info)() - 2*panedwindow['bd'] \
                            - panedwindow['sashpad'] - panedwindow['sashwidth'] \
                            - size            
        else:
            sash_index = index - 1
            new_position = panedwindow.sash_coord(index)[position_coord] \
                            - panedwindow['sashpad'] - panedwindow['sashwidth'] \
                            - size

        sash_coordinates[position_coord] = new_position
            
        panedwindow.sash_place(sash_index, *sash_coordinates)

    def __get_pane_size_in_panedwindow(self, panedwindow, index):
        if panedwindow['orient'] == HORIZONTAL:
            # Coordinate X
            position_coord = 0
                
            method_for_size_info = 'winfo_reqwidth'
        else:
            # Coordinate Y
            position_coord = 1
                
            method_for_size_info = 'winfo_reqwidth'
            
        last_index = len(panedwindow.panes()) - 1 
                            
        if index == 0:
            pane_size = panedwindow.sash_coord(index)[position_coord]
        elif index == last_index:
            pane_size = getattr(panedwindow, method_for_size_info)() - 2*panedwindow['bd'] \
                        - panedwindow.sash_coord(index-1)[position_coord] \
                        - panedwindow['sashpad'] - panedwindow['sashwidth']
        else:
            pane_size = panedwindow.sash_coord(index)[position_coord] \
                        - panedwindow.sash_coord(index-1)[position_coord] \
                        - panedwindow['sashpad'] - panedwindow['sashwidth']
                    
        return pane_size
        
    def get_row_height(self, row):
        if self.calculate_dimensions:
            self.__calculate_list_of_cell_widths_and_heights()

        if self.orient == VERTICAL:
            if self.is_builded:
                if self.is_a_fixed_pane(row):
                    return self.__rowHeights[row]
                else:
                    return self.__get_mobile_pane_size(row)
            else:
                return self.__rowHeights[row]
        else:
            return self.__rowHeights[row]

    def get_column_width(self, column):
        if self.calculate_dimensions:
            self.__calculate_list_of_cell_widths_and_heights()
        if self.orient == HORIZONTAL:
            if self.is_builded:
                if self.is_a_fixed_pane(column):
                    return self.__columnWidths[column]
                else:
                    return self.__get_mobile_pane_size(column)
            else:
                return self.__columnWidths[column]
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
        if self.is_builded:
            raise Exception("The GridWithPanes was is_builded. Use cell_update() instead.")

        i , j = self.check_coordinates(coordinates)

        self.__gridOfWidgets[i,j] = widget

        self.__rows[i].add(j)
        self.__columns[j].add(i)

        self.calculate_dimensions = True

    def __delitem__(self, coordinates ):
        if self.is_builded:
            raise Exception("The GridWithPanes was is_builded. Use cell_update() instead.")

        i, j = self.check_coordinates(coordinates)

        del self.__gridOfWidgets[i,j]

        self.__rows[i].discard(j)
        if not self.__rows[i]: del self.__rows[i]

        self.__columns[j].discard(i)
        if not self.__columns[j]: del self.__columns[j]

        self.calculate_dimensions = True

    def grid(self, *args, **kargs):
        if not self.is_builded: self.build()
        Frame.grid(self,*args, **kargs)
        self.is_displayed = True
        
    def pack(self, *args, **kargs):
        if not self.is_builded: self.build()
        Frame.pack(self,*args, **kargs)
        self.is_displayed = True

    def place(self, *args, **kargs):
        if not self.is_builded: self.build()
        Frame.place(self,*args, **kargs)
        self.is_displayed = True

def test():
    try:
        from tkinter import ttk
    except ImportError:
        import ttk
            
    root = Tk()

    def table_of_random_widgets(master, numRows,numColumns, **kwargs):
        import random
        demo = GridWithPanes(master, **kwargs)

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

    Label(root, text="orient=VERTICAL, minsize = 20, fixed rows = [2,5]").pack(anchor=NW, pady=6, padx='2m')
    table1 = table_of_random_widgets(root, numRows=6,numColumns=5, orient=VERTICAL, minsize=20, fixedPanes=[2,5])
    table1.pack(anchor=NW,pady=2, padx='2m')

    emptySpace = Frame(root, height =20)
    emptySpace.pack()


    Label(root, text='''orient=HORIZONTAL, minsize = 30, fixed columns = [2], columnWidths={0:200, 2: 150, 3:250}, rowHeights={0:150}\nOn this table we will update later the cell (1,2)''', justify=LEFT).pack(anchor=NW, pady=6, padx='2m')

    table2 = table_of_random_widgets(root, numRows=3,numColumns=6, minsize=30, fixedPanes=[2], columnWidths={0:200, 2: 150, 3:250}, rowHeights={0:90})
    table2.pack(anchor=NW,pady=2, padx='2m')

    table2.update_cell((1,2), Label(table2,text="Cell updated",bg="green") )

    emptySpace = Frame(root, height =20)
    emptySpace.pack()

    def show_table_data():
        tableName = TableVar.get()
        if tableName=='top table':
            table = table1
        elif tableName=='bottom table':
            table = table2
        else:
            return
        
        StringData = ""
        
        StringData += "Data of the grid with panes:\n"
        StringData += "\tnumber of rows: %d\n" % table.numberOfRows
        StringData +="\tnumber of columns: %d\n" % table.numberOfColumns
        StringData +="\tTable width: %d\n" % table.tableWidth
        StringData +="\tTable height: %d\n" % table.tableHeight
    
        StringData +="\n\tHeights:\n"
    
        for row in table.rowIndices:
            StringData += "\t\trow %s: %s\n" % (row, table.get_row_height(row) ) 
    
        StringData +="\n\tWidths:\n"
    
        for column in table.columnIndices:
            StringData += "\t\tcolumn %s: %s\n" % (column, table.get_column_width(column) )

        print( StringData)

    def change_pane_size():
        tableName = TableVar.get()
        
        if tableName=='top table':
            table = table1
        elif tableName=='bottom table':
            table = table2
        else:
            return

        if table.orient == HORIZONTAL:
            table.columnconfigure(PaneVar.get(),SizeVar.get() ) 
        else:
            table.rowconfigure(PaneVar.get(),SizeVar.get() ) 

    emptySpace = Frame(root, height =40)
    emptySpace.pack()
    
    ControlArea = LabelFrame(root, text ="Control area", labelanchor=N)
    ControlArea.pack(expand=YES, fill=X, padx=20)

    ControlArea1 = Frame(ControlArea)
    ControlArea1.pack(expand=YES, fill=X, padx = 13)
        
    Button(ControlArea1, text="Show data of widget on console", command= lambda : show_table_data() ).pack(side=LEFT)
    
    ControlArea2 = Frame(ControlArea)
    ControlArea2.pack(expand=YES, fill=X, padx = 13)

    Label(ControlArea2, text="Table: ").pack(side=LEFT)
    TableVar = StringVar()
    TableVar.set('top table')
    OptionMenu(ControlArea2, TableVar,'top table', 'bottom table').pack(side=LEFT)

    
    Label(ControlArea2, text="Pane index: ").pack(side=LEFT)
    PaneVar = IntVar()
    Pane_entry = Entry(ControlArea2, textvariable = PaneVar, width=2)
    Pane_entry.pack(side=LEFT)
    Pane_entry.bind('<Return>',  lambda event: change_pane_size() )
    Pane_entry.focus()
    
    
    Label(ControlArea2, text="Size: ").pack(side=LEFT)
    SizeVar = IntVar()
    Size_entry = Entry(ControlArea2, textvariable = SizeVar, width=4)
    Size_entry.pack(side=LEFT)
    Size_entry.bind('<Return>',  lambda event: change_pane_size() )
    
    
    Button(ControlArea2, text="Change pane size", command = lambda: change_pane_size() ).pack(side=LEFT)
    
    root.mainloop()


if __name__ == '__main__':
    test()
