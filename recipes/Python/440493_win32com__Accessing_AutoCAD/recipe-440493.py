import win32com.client
acad = win32com.client.Dispatch("AutoCAD.Application")

doc = acad.ActiveDocument   # Document object
ms = doc.ModelSpace         # Modelspace "collection"
count = ms.Count            # Number of items in modelspace

for i in range(count):
    item = ms.Item(i)
    if 'text' in item.ObjectName.lower(): # Text objects are AcDbText
        # once we know what it is we can cast it
        text = win32com.client.CastTo(item, "IAcadText") 
        if text.TextString == "Spam":
            text.TextString = "Maps"
            text.Update()
