import pyoocalc

# open document
doc = pyoocalc.Document()
file_name = os.getcwd() + "/example.ods"
doc.open_document(file_name)

# Get document fields
fields = doc.fields()

# Get field "HEADER"
field = fields.field("HEADER")
print ("Document header is: " + str(field.is_null()))

# Set values
field = fields.field("TABLE_NAME")
field.set_value("Test table name")
print ("New table name is: " + field.value())

# Insert 5 rows
field1 = fields.field("FIELD_1")
num_rows = 5
step = 2
if num_rows > 0:
    field1.insert_rows(num_rows=num_rows-1, step=step, columns_to_copy=200)
for i in range(1, num_rows + 1):
    field1.set_value("F1." + str(i), 0, i * step - (step - 1))

# Set value="value1" at column=1, row=1 (B1)
sheet = doc.sheets().sheet(0)
sheet.set_cell_value_by_index(1, 0, "value1")
print (sheet.cell_value_by_index(1, 0))
del doc
