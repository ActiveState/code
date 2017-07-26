		# attempt to attach to the database - if that fails, create a new one
		# use the file name as the base name for the database
		self.dbName = os.path.splitext(fileName)[0]
		dsn = 'Provider=Microsoft.Jet.OLEDB.4.0;' + \
				'Jet OLEDB:Engine Type=5;' + \
				'Data Source=' + 'test.mdb'

		# try to create the database
		catalog = win32com.client.Dispatch('ADOX.Catalog') 
		try:
			catalog.Create(dsn)
			catalog.ActiveConnection = dsn
		except:
			raise "Can't connect to database table"


		# create a table with the appropriate field names
		table = win32com.client.Dispatch('ADOX.Table') 
		self.rs = win32com.client.Dispatch('ADODB.Recordset')
		table.Name = "TabName"

		Column = win32com.client.Dispatch("ADOX.Column")
		Column.Name = "AutoNumber"
		Column.Type = 3 # adInteger
		Column.ParentCatalog = catalog
		Column.Properties('Autoincrement').Value = win32com.client.pywintypes.TRUE
		table.Columns.Append(Column)

		Key = win32com.client.Dispatch("ADOX.Key")
		Key.Name = "PrimaryKey"
		Key.Type = 1 #win32.com.client.constants.adKeyPrimary
		Key.RelatedTable = "TabName"
		Key.Columns.append("AutoNumber")
		table.Keys.Append(Key)

		# add other fields using table.Columns.Append()


		catalog.Tables.Append(table)
		del table
		del catalog
