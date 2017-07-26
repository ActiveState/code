-----------------  Test.py  -----------------
from FML import Table

print "Content-Type: text/html\n\n"

T = Table()
T.AddHeader("Head 1", "Head 2")

T.TableName = "Fedmich..."
T.Collapsable = 1

T.AddRow("1", "<i>2</i>")
T.AddRow("3", "<b>4</b>")
T.AddRow("5", "6")

print T.result()


print "<br>"
T.TableName = "Fedmich 2..."
T.headers = []
T.AddHeader("HTop", "HTop2")
T.AddHeader2("Head_Below", "Head_Below 2")
T.ClearRows()
T.Color = "Green"

for i in range(1, 20):
    T.AddRow(i, "... | width=400")  #Custom Attribute...

T.Highlight(6)

T.Select(10)

print T.result()


-----------------  FML.py  -----------------
##  FML which means - FedHTML (python version)
##  by  Fedmich
##  version 1.1
##  Last modified:  10:57 AM 5/19/2006

## Configurations...
src1 = "/images/triangle_open.gif"
src2 = "/images/triangle_closed.gif"
imgfol = "/images/"
                

from glob import fnmatch
Like = fnmatch.fnmatch

TableGenerated = 0

#used for script & styles inclusions, 1 occurence only.

global _TS_OK, _SC_Toggle
_TS_OK = 0      ##  TableStyle
_SC_Toggle = 0  ##ScriptToggle

def InLocal(objName):
    return len([elem for elem in locals() if elem.lower() == objName.lower() ])
def InGlobals(objName):
    return len([elem for elem in globals() if elem.lower() == objName.lower() ])

def iif(condition,resultiftrue,resultiffalse):
    if condition:return resultiftrue
    else: return resultiffalse
    
def GetQuery(QueryString, BlankIfMissing =0 ):
    if not InGlobals("FormFieldStorage"):
        from cgi import FieldStorage
        global FormFieldStorage
        FormFieldStorage = FieldStorage()

    if FormFieldStorage.has_key(QueryString):
        retVal = FormFieldStorage[QueryString].value
    else:
        retVal = iif(BlankIfMissing,"",None)

    return retVal
    
def CheckAttrib(HTML):
    sHTML = str(HTML)
    if Like(sHTML, "* | *"):
        sp = sHTML.split(" | ")
        ActualText = sp[0]
        ExtraAttrb = sp[1]
        return (ActualText,ExtraAttrb)
    else:
        return (sHTML,"")
    
class Table:
    def __init__(self, TableAttr = ""):
        self.datas = []
        self.headers = []
        self.headers2 = []
        self.rowcount = 0
        self.selected = []
        self.highlighted = []
        self.TableName = ""
        self.TableAttrib = TableAttr
        self.Collapsable = 0
        self.Collapsed = 0
        self.Color = "blue"

    def ClearRows(self):
        self.datas = []
        self.rowcount = 0
        
    def AddRow(self, *rowdatas):
        self.datas.append(rowdatas)
        self.rowcount = len(self.datas)

    def AddHeader(self, *Headers):
        self.headers.append(Headers)
    def AddHeader2(self, *Headers):
        self.headers2.append(Headers)

    def Select(self, index):
        li = self.selected
        if index not in li:
            li.append(index)
        
    def Highlight(self, index):
        li = self.highlighted
        if index not in li:
            li.append(index)
            
    def result(self):
        global _TS_OK
        if not _TS_OK:
            TableStyle = """
                <STYLE>
                .Header{
                    background-color: #C3D9FF;
                }        
                .Normal{
                    background-color: #E8EEF7;
                }
                .Selected{
                    font-weight: bold;
                    background-color: #FFFFCC 
                }
                .Highlight {
                    background-color : #FFFFFF;
                    font-weight: bold;
                }
                .MousePointed{
                    background-color: #FFFFFF;
                }
                </STYLE>"""
            print TableStyle
            _TS_OK = 1
        
        output = ""
        if self.TableName <> "":
            if self.Collapsable:
                global _SC_Toggle
                if not _SC_Toggle:
                    ScriptToggle = """<script language="javascript">
                    function ToggleSpan(oSpan, oSpanImg){
                            if (oSpan == null)
                                return false
                                
                            if (oSpan.style.display == "none")
                                oSpan.style.display = "block"
                            else
                                oSpan.style.display = "none"
                            
                            if (oSpanImg != null){
                                src1 = "%s"
                                src2 = "%s"
                                
                                if (oSpanImg.src.match('open'))
                                    oSpanImg.src = src2
                                else
                                    oSpanImg.src = src1
                            }
                        }
                    </script>""" % ( src1, src2)
                    _SC_Toggle = 1
                    print ScriptToggle
                
                global TableGenerated
                TableGenerated += 1
                TableId = TableGenerated
                
                if self.Collapsed:
                    srcIMG = src2
                else:
                    srcIMG = src1
                
                IMGTria = "<img id='TableTria%s' src='%s' border=0 width=11 height=11>" % (TableId, srcIMG)
                output += """<a href='#FedTable' STYLE="text-decoration:none"
                            onclick="hasfunc=0; try{
                            ToggleSpan(document.getElementById('Table%s'),
                                       document.getElementById('TableTria%s'))}
                                       catch(e){} ;
                            ">%s
                            """ % (TableId, TableId, IMGTria)
                            
            output += "<b>%s</b>" % self.TableName

            if self.Collapsable:
                spanX = ""
                if self.Collapsed:
                    spanX = "style='display:None'"
                output += "</a><span id='Table%s' %s>" % (TableId, spanX)
        
        if self.TableAttrib <> "":
            output += "<table %s>\n" % self.TableAttrib 
        else:
            output += "<table border=0 cellspacing=1 celpadding=0>\n"

        HeaderCount = 0

        for hCounter in range(0,2):
            if hCounter==0:
                Headers = self.headers
            else:
                Headers = self.headers2
                
            if len(Headers):
                output += "<TR>\n"
                if type(Headers) is list:
                    for head in Headers:
                        for h in head:
                            (hName, ExtraAttrb) = CheckAttrib(h)
                            
                            output += "<th class='%s' %s>%s</th>\n" % ("Header", ExtraAttrb, hName)
                else:
                    output += "<th>%s</th>\n" % Headers

                if hCounter==0:
                    HeaderCount = 1
                        
                output += "</TR>\n"

        selcount = len(self.selected)
        highcount = len(self.highlighted)
        for i in range(0, len(self.datas)):
            row = self.datas[i]
            ClassName = "Normal"
            
            if (i +1) in self.selected:
                ClassName = "Selected"
            if (i +1) in self.highlighted:
                ClassName = "Highlight"

            (tdName, ExtraAttrb) = ("","")
            finTD = 0        
            output += """<tr class='%s'
                    onMouseOver="this.className='MousePointed'" onMouseOut="this.className='%s'">\n""" % (ClassName,ClassName)
            lRow = len(row)
            for td in row:
                li_tds = td
                if not type(td) is list:
                    li_tds = [td]

                for tds in li_tds:
                    (tdName, ExtraAttrb) = CheckAttrib(tds)
                    output += "<td %s>%s</td>\n" % (ExtraAttrb, tdName)
            
            output += "</tr>\n"
            
        output += "</table>\n"

        if self.Collapsable:
            output += "</span>"
            output = RoundEdge(output, self.Color)
        
        return output

def RoundEdge(contents, color="green"):
    result = """
    <table cellspacing="0" cellpadding="0" border="0">
      <tr>
        <td width=8 height=8 style="background:url(<imgfol>edges/<col>_e1.gif)">
        <img src="<imgfol>edges/spacer.gif" width=8 height=8 alt="" /></td>
        <td width="100%%" height=8 style="background:url(<imgfol>edges/<col>_e2.gif)"><img src="<imgfol>edges/spacer.gif" width=1 height=8 alt="" /></td>
        <td width=8 height=8 style="background:url(<imgfol>edges/<col>_e3.gif)"><img src="<imgfol>edges/spacer.gif" width=8 height=8 alt="" /></td>
      </tr>
      <tr>
        <td width=8 style="background:url(<imgfol>edges/<col>_e4.gif)"><img src="<imgfol>edges/spacer.gif" width=8 height=1 alt="" /></td>
        <td>%s</td>
        <td width=8 style="background:url(<imgfol>edges/<col>_e5.gif)"><img src="<imgfol>edges/spacer.gif" width=8 height=1 alt="" /></td>
      </tr>
      <tr>
        <td width=8 height=8 style="background:url(<imgfol>edges/<col>_e6.gif)"><img src="<imgfol>edges/spacer.gif" width=8 height=8 alt="" /></td>
        <td height=8 style="background:url(<imgfol>edges/<col>_e7.gif)"><img src="<imgfol>edges/spacer.gif" width=1 height=8 alt="" /></td>
        <td width=8 height=8 style="background:url(<imgfol>edges/<col>_e8.gif)"><img src="<imgfol>edges/spacer.gif" width=8 height=8 alt="" /></td>
      </tr> 
    </table>
    """
    result = result.replace("<imgfol>", imgfol)
    result = result.replace("<col>", color)
    result = result % contents
    return result
