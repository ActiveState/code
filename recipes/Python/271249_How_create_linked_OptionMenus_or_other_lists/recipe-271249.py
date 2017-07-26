#file linkedOptionMenus.py
#Stewart Midwinter, stewart 'at' midwinter 'dot' ca
#thanks to Eric Brunel and Peter Otten
#use and enjoy!

title = 'linked OptionMenus'

# Import Pmw from this directory tree.
import sys
sys.path[:0] = ['../../..']

import Tkinter
import Pmw, re

global continentList, countryList, stateList

continentList = ['N.America','C. America', 'S. America']
countryList   = {'N.America':['Canada','USA','Mexico'],
		 'C. America':['Guatemala','Nicaragua','Panama'],
		 'S. America':['Venezuela','Colombia','Ecuador']
		 }
stateList     = {'Canada':['BC','Alberta','Saskatchewan','Manitoba','Ontario','Quebec',
                    'New Brunswick','Nova Scotia','Prince Edward Island','Newfoundland',
                    'Nunavut','Northwest Territory'],
		 'USA':['California','Oregon','Washington','others'],
		 'Mexico':['Aguascalientes', 'Baja California', 'Baja California Sur', 
                     'Campeche', 'Chiapas', 'Chihuahua', 'Coahuila de Zaragoza', 'Colima', 
                     'Distrito Federal', 'Durango', 'Guanajuato', 'Guerrero', 'Hidalgo', 
                     'Jalisco', 'Mexico', 'Michoacan de Ocampo', 'Morelos', 'Nayarit', 
                     'Nuevo Leon', 'Oaxaca', 'Puebla', 'Queretaro de Arteaga', 'Quintana Roo', 
                     'San Luis Potosi', 'Sinaloa', 'Sonora', 'Tabasco', 'Tamaulipas', 'Tlaxcala', 
                     'Veracruz-Llave', 'Yucatan', 'Zacatecas'],
		 'Guatemala':['Alta Verapaz', 'Baja Verapaz', 'Chimaltenango', 
                     'Chiquimula', 'El Progreso', 'Escuintla', 'Guatemala', 
                     'Huehuetenango', 'Izabal', 'Jalapa', 'Jutiapa', 'Peten', 
                     'Quetzaltenango', 'Quiche', 'Retalhuleu', 'Sacatepequez', 
                     'San Marcos', 'Santa Rosa', 'Solola', 'Suchitepequez', 
                     'Totonicapan', 'Zacapa'],
		 'Nicaragua':['Boaco', 'Carazo', 'Chinandega', 'Chontales', 'Esteli', 'Granada', 
                     'Jinotega', 'Leon', 'Madriz', 'Managua', 'Masaya', 'Matagalpa', 'Nueva Segovia', 
                     'Rio San Juan', 'Rivas', 'Atlantico Norte*', 'Atlantico Sur*'],
		 'Panama':['Bocas del Toro', 'Chiriqui', 'Cocle', 'Colon', 'Darien', 
                     'Herrera', 'Los Santos', 'Panama', 'San Blas*', 'Veraguas'],
		 'Venezuela':['Amazonas', 'Anzoategui', 'Apure', 'Aragua', 'Barinas', 'Bolivar', 
                     'Carabobo', 'Cojedes', 'Delta Amacuro', 'Falcon', 'Guarico', 'Lara', 'Merida', 
                     'Miranda', 'Monagas', 'Nueva Esparta', 'Portuguesa', 'Sucre', 
                     'Tachira', 'Trujillo', 'Vargas', 'Yaracuy', 'Zulia'],
		 'Colombia':['Amazonas', 'Antioquia', 'Arauca', 'Atlantico', 
                     'Bolivar', 'Boyaca', 'Caldas', 'Caqueta', 'Casanare', 
                     'Cauca', 'Cesar', 'Choco', 'Cordoba', 'Cundinamarca', 
                     'Guainia', 'Guaviare', 'Huila', 'La Guajira', 'Magdalena', 
                     'Meta', 'Narino', 'Norte de Santander', 'Putumayo', 'Quindio', 
                     'Risaralda', 'San Andres y Providencia', 
                     'Distrito Capital de Santa Fe de Bogota', 'Santander', 
                     'Sucre', 'Tolima', 'Valle del Cauca', 'Vaupes', 'Vichada'],
		 'Ecuador':['Ecuador states']
		 }

# default selection
continentItem = continentList[0]
countryItem = countryList[continentItem][0]
stateItem = stateList[countryItem][0]

class selectSystem:
    def __init__(self, parent):
	# Create and pack the OptionMenu megawidgets.
	# The first one has a textvariable.
	self.varContinent = Tkinter.StringVar()
	self.varCountry = Tkinter.StringVar()
	self.varState = Tkinter.StringVar()
	self.varContinent.set(continentItem)	# N. America
	self.varCountry.set(countryItem)	# Canada
	self.varState.set(stateItem)	# B.C.

	self.continent_menu = Pmw.OptionMenu(parent,
		labelpos = 'w',
		label_text = 'Select Continent:',
		menubutton_textvariable = self.varContinent,
		items = continentList,
		menubutton_width = 20,
		menubutton_direction = 'flush',
		command = self._selectContinent
	)
	self.continent_menu.pack(anchor = 'w', padx = 10, pady = 10)

	self.country_menu = Pmw.OptionMenu (parent,
		labelpos = 'w',
		label_text = 'Select country:',
		menubutton_textvariable = self.varCountry,
		items = countryList['N.America'],
		menubutton_width = 20,
		menubutton_direction = 'flush',
		command = self._selectCountry
	)
	self.country_menu.pack(anchor = 'w', padx = 10, pady = 10)

	self.state_menu = Pmw.OptionMenu (parent,
		labelpos = 'w',
		label_text = 'Select state:',
		menubutton_textvariable = self.varState,
		items = stateList['Canada'],
		menubutton_width = 20,
		menubutton_direction = 'flush' ,
		command = self._getSelection
	)
	self.state_menu.pack(anchor = 'w', padx = 10, pady = 10)

	menus = (self.continent_menu, self.country_menu, self.state_menu)
	Pmw.alignlabels(menus)

	# Create the dialog.
	self.dialog = Pmw.Dialog(parent,
	    buttons = ('OK', 'Apply', 'Cancel', 'Help'),
	    defaultbutton = 'OK',
	    title = 'Select State',
	    command = self.execute)
	self.dialog.withdraw()

	# Add some contents to the dialog.
	w = Tkinter.Label(self.dialog.interior(),
	    text = 'Pmw Dialog\n(put your widgets here)',
	    background = 'black',
	    foreground = 'white',
	    pady = 20)
	w.pack(expand = 1, fill = 'both', padx = 4, pady = 4)

    def showAppModal(self):
        self.dialog.activate(geometry = 'centerscreenalways')

    def execute(self, result):
	print 'You clicked on', result
	if result not in ('Apply', 'Help'):
	    self.dialog.deactivate(result)

    def _getSelection(self, choice):
	# Can use 'self.var.get()' instead of 'getcurselection()'.
	print 'You have chosen %s : %s : %s' % \
            (self.varContinent.get(), 
	     self.varCountry.get(), 
	     self.varState.get() )
	print choice  # debug

    def _selectContinent(self, choice):
	## Set appropriate list of countries
	countries = countryList[self.varContinent.get()]
	self.country_menu.setitems(countries)
	## If currently selected country is not in new list, select first valid one
	if not self.varCountry.get() in countries:
		self.varCountry.set(countries[0])
	## Set appropriate list of states
	states = stateList[self.varCountry.get()]
	self.state_menu.setitems(states)
	## If currently selected state is not in list, select first valid one
	if not self.varState.get() in states:
		self.varState.set(states[0])

    def _selectCountry(self, choice):
	## Set appropriate list of states
	states = stateList[self.varCountry.get()]
	self.state_menu.setitems(states)
	## If currently selected state is not in list, select first valid one
	if not self.varState.get() in states:
		self.varState.set(states[0])


    def __call__(self):
	self.dialog.show()

def indexContinent(name):
	found = 'false'
	for i in range(len(continentList)):
		check = continentList[i]
		# print 'checking %s in %s' % (name, check)  # debug
		if re.search(name,check):
			found = 'true'
			break
	print found
	if (found=='true'):
		#print 'index of %s is %s' % (name,i)  # debug
		return i
	else:
		return -1

def indexCountry(continentindex, name):
	found = 'false'
	for i in range(len(countryList[continentindex])):
		check = countryList[continentindex][i]
		# print 'checking %s in %s' % (name, check)  # debug
		if re.search(name,check):
			found = 'true'
			break
	print found
	if (found=='true'):
		#print 'index of %s is %s' % (name,i)  # debug
		return i
	else:
		return -1


######################################################################

# Create selectSystem in root window for testing.
if __name__ == '__main__':
    root = Tkinter.Tk()
    Pmw.initialise(root)
    root.title(title)

    OKButton = Tkinter.Button(root, text = 'OK', command = root.destroy)
    OKButton.pack(side = 'bottom')

    widget = selectSystem(root)
    root.mainloop()
