          Paper 1 / White Spaces are included
  Single Correct Answer Type

1. Text of question 1
  a) Option 1.a    b) Option 1.b
  c) Option 1.c    d) Option 1.d

2. Text of question 2
  a) This is an example of Option 2.a
  b) Option 2.b has a special char α
  c) Option 2.c
  d) Option 2.d

3. Text of question 3
  a) Option 3.a can span multiple
  lines.
  b) Option 3b
  c) Option 3c
  d) Option 3d

My code:

    from lxml import etree
    import csv

    root = etree.Element('data')
    #f = open('input1.txt','rb')
    rdr = csv.reader(open("input1.txt",newline='\n'))
    header = next(rdr)
    for row in rdr:
        eg = etree.SubElement(root, 'eg')
        for h, v in zip(header, row):
            etree.SubElement(eg, h).text = v

     f = open(r"C:\temp\input1.xml", "w")
     f.write(etree.tostring(root))
     f.close()

I'm getting an error like:

    Traceback (most recent call last):
      File "E:\python3.2\input1.py", line 11, in <module>
        etree.SubElement(eg, h).text = v
      File "lxml.etree.pyx", line 2995, in lxml.etree.SubElement (src\lxml\lxml.etree.c:69677)
      File "apihelpers.pxi", line 188, in lxml.etree._makeSubElement (src\lxml\lxml.etree.c:15691)
      File "apihelpers.pxi", line 1571, in lxml.etree._tagValidOrRaise (src\lxml\lxml.etree.c:29249)
    ValueError: Invalid tag name 'ï»¿    Paper 1'
    
