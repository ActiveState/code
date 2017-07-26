import win32com.client
catapp = win32com.client.Dispatch("CATIA.Application")
doc=catapp.ActiveDocument.Product

product_count = doc.Products.Count
print "This example lists all Parts and Subproducts of the first level from a CATProduct."
for products in range(product_count):
    products = products + 1
    print doc.Products.Item(products).Name, ":"
    part_count = doc.Products.Item(products).Products.Count
    for parts in range(part_count):
        parts = parts +1
        print "   ", doc.Products.Item(products).Products.Item(parts).Name

#For aHTML-generated Bill of Material you should use doc.Product.ExtractBOM(2, 'c:\\BOM.html') 
