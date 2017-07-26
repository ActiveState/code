>>> import fitz
>>> doc = fitz.open("pymupdf.pdf")
>>> page = doc[6]                   # page 6 contains 4 links
>>> lnks = page.getLinks()
>>> 
>>> #----------------------------------------------------------------------------------------------
>>> # first, display the links we have
>>> #----------------------------------------------------------------------------------------------
>>> for l in lnks:
        print(l)
{'kind': 2, 'xref': 864, 'from': fitz.Rect(249.714, 142.312,
295.942, 154.063), 'type': 'uri', 'uri': 'https://github.com/rk700/PyMuPDF'}
{'kind': 2, 'xref': 1090, 'from': fitz.Rect(255.626, 257.481,
301.854, 269.231), 'type': 'uri',
'uri': 'https://github.com/JorjMcKie/PyMuPDF-optional-material'}
{'kind': 2, 'xref': 978, 'from': fitz.Rect(183.562, 325.227,
206.773, 336.977), 'type': 'uri',
'uri': 'https://pypi.python.org/pypi?:action=display&name=PyMuPDF&version=1.10.0'}
{'kind': 2, 'xref': 1059, 'from': fitz.Rect(383.579, 526.211,
430.582, 537.961), 'type': 'uri', 'uri': 'https://en.wikipedia.org/wiki/MuPDF'}
>>> 
>>> #----------------------------------------------------------------------------------------------
>>> # delete last link on page and display again
>>> #----------------------------------------------------------------------------------------------
>>> l = lnks[-1]
>>> page.deleteLink(l)
>>> for l in page.getLinks():
    print(l)
{'kind': 2, 'xref': 864, 'from': fitz.Rect(249.714, 142.312,
295.942, 154.063), 'type': 'uri', 'uri': 'https://github.com/rk700/PyMuPDF'}
{'kind': 2, 'xref': 1090, 'from': fitz.Rect(255.626, 257.481,
301.854, 269.231), 'type': 'uri',
'uri': 'https://github.com/JorjMcKie/PyMuPDF-optional-material'}
{'kind': 2, 'xref': 978, 'from': fitz.Rect(183.562, 325.227,
206.773, 336.977), 'type': 'uri',
'uri': 'https://pypi.python.org/pypi?:action=display&name=PyMuPDF&version=1.10.0'}
>>>
>>> #----------------------------------------------------------------------------------------------
>>> # now change first link to point to somewhere on page 1 of same file
>>> #----------------------------------------------------------------------------------------------
>>> l = lnks[0]
>>> l["kind"] = fitz.LINK_GOTO
>>> l["page"] = 1
>>> l["to"] = fitz.Point(100, 200)
>>> page.updateLink(l)
>>> for l in page.getLinks():
    print(l)
{'kind': 1, 'xref': 864, 'from': fitz.Rect(249.714, 142.312,
295.942, 154.063), 'type': 'goto', 'page': 1, 'to': fitz.Point(100.0, 200.0), 'zoom': 0.0}
{'kind': 2, 'xref': 1090, 'from': fitz.Rect(255.626, 257.481,
301.854, 269.231), 'type': 'uri',
'uri': 'https://github.com/JorjMcKie/PyMuPDF-optional-material'}
{'kind': 2, 'xref': 978, 'from': fitz.Rect(183.562, 325.227,
206.773, 336.977), 'type': 'uri', 
'uri': 'https://pypi.python.org/pypi?:action=display&name=PyMuPDF&version=1.10.0'}
>>>
>>> #----------------------------------------------------------------------------------------------
>>> # now insert a new link to open another file
>>> #----------------------------------------------------------------------------------------------
>>> l = lnks[3]                      # reuse rectangle of deleted link above
>>> l["kind"] = fitz.LINK_LAUNCH
>>> l["file"] = "some.file"
>>> page.insertLink(l)
>>> for l in page.getLinks():
    print(l)
{'kind': 1, 'xref': 864, 'from': fitz.Rect(249.714, 142.312,
295.942, 154.063), 'type': 'goto', 'page': 1, 'to': fitz.Point(100.0, 200.0), 'zoom': 0.0}
{'kind': 2, 'xref': 1090, 'from': fitz.Rect(255.626, 257.481,
301.854, 269.231), 'type': 'uri',
'uri': 'https://github.com/JorjMcKie/PyMuPDF-optional-material'}
{'kind': 2, 'xref': 978, 'from': fitz.Rect(183.562, 325.227,
206.773, 336.977), 'type': 'uri',
'uri': 'https://pypi.python.org/pypi?:action=display&name=PyMuPDF&version=1.10.0'}
{'kind': 3, 'xref': 1251, 'from': fitz.Rect(383.579, 526.211,
430.582, 537.961), 'type': 'launch', 'file': 'some.file'}
>>> # the PDF must be saved to make these changes permanent
>>> doc.saveIncr()                   # incremental save back to original file
