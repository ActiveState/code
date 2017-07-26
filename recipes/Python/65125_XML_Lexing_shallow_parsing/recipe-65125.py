import re

class recollector:
    def __init__(self):
        self.res={}
    def add(self, name, reg ):
        re.compile(reg) # check that it is valid

        self.res[name] = reg % self.res
        
collector = recollector()
a = collector.add

a("TextSE" , "[^<]+")
a("UntilHyphen" , "[^-]*-")
a("Until2Hyphens" , "%(UntilHyphen)s(?:[^-]%(UntilHyphen)s)*-")
a("CommentCE" , "%(Until2Hyphens)s>?") 
a("UntilRSBs" , "[^\\]]*](?:[^\\]]+])*]+")
a("CDATA_CE" , "%(UntilRSBs)s(?:[^\\]>]%(UntilRSBs)s)*>" )
a("S" , "[ \\n\\t\\r]+")
a("NameStrt" , "[A-Za-z_:]|[^\\x00-\\x7F]")
a("NameChar" , "[A-Za-z0-9_:.-]|[^\\x00-\\x7F]")
a("Name" , "(?:%(NameStrt)s)(?:%(NameChar)s)*")
a("QuoteSE" , "\"[^\"]*\"|'[^']*'")
a("DT_IdentSE" , "%(S)s%(Name)s(?:%(S)s(?:%(Name)s|%(QuoteSE)s))*" )
a("MarkupDeclCE" , "(?:[^\\]\"'><]+|%(QuoteSE)s)*>" )
a("S1" , "[\\n\\r\\t ]")
a("UntilQMs" , "[^?]*\\?+")
a("PI_Tail" , "\\?>|%(S1)s%(UntilQMs)s(?:[^>?]%(UntilQMs)s)*>" )
a("DT_ItemSE" ,
    "<(?:!(?:--%(Until2Hyphens)s>|[^-]%(MarkupDeclCE)s)|\\?%(Name)s(?:%(PI_Tail)s))|%%%(Name)s;|%(S)s"
)
a("DocTypeCE" ,
"%(DT_IdentSE)s(?:%(S)s)?(?:\\[(?:%(DT_ItemSE)s)*](?:%(S)s)?)?>?" )
a("DeclCE" ,
    "--(?:%(CommentCE)s)?|\\[CDATA\\[(?:%(CDATA_CE)s)?|DOCTYPE(?:%(DocTypeCE)s)?")
a("PI_CE" , "%(Name)s(?:%(PI_Tail)s)?")
a("EndTagCE" , "%(Name)s(?:%(S)s)?>?")
a("AttValSE" , "\"[^<\"]*\"|'[^<']*'")
a("ElemTagCE" ,
    "%(Name)s(?:%(S)s%(Name)s(?:%(S)s)?=(?:%(S)s)?(?:%(AttValSE)s))*(?:%(S)s)?/?>?")

a("MarkupSPE" ,
    "<(?:!(?:%(DeclCE)s)?|\\?(?:%(PI_CE)s)?|/(?:%(EndTagCE)s)?|(?:%(ElemTagCE)s)?)")
a("XML_SPE" , "%(TextSE)s|%(MarkupSPE)s")
a("XML_MARKUP_ONLY_SPE" , "%(MarkupSPE)s")


def lexxml(data, markuponly=0):
    if markuponly:
        reg = "XML_MARKUP_ONLY_SPE"
    else:
        reg = "XML_SPE"
    regex = re.compile(collector.res[reg])
    return regex.findall(data)

def assertlex(data, numtokens, markuponly=0):
    tokens = lexxml(data, markuponly)
    if len(tokens)!=numtokens:
        assert len(lexxml(data))==numtokens,            "data = '%s', numtokens = '%s'" %(data, numotkens)
    if not markuponly:
        assert "".join(tokens)==data
    walktokens(tokens)

def walktokens(tokens):
    print
    for token in tokens:
        if token.startswith("<"):
            if token.startswith("<!"):
                print "declaration:", token
            elif token.startswith("<?xml"):
                print "xml declaration:", token
            elif token.startswith("<?"):
                print "processing instruction:", token
            elif token.startswith("</"):
                print "end-tag:", token
            elif token.endswith("/>"):
                print "empty-tag:", token
            elif token.endswith(">"):
                print "start-tag:", token
            else:
                print "error:", token
        else:
            print "text:", token

def testlexer():
    # this test suite could be larger!
    assertlex("<abc/>", 1)
    assertlex("<abc><def/></abc>", 3)
    assertlex("<abc>Blah</abc>", 3)
    assertlex("<abc>Blah</abc>", 2, markuponly=1)
    assertlex("<?xml version='1.0'?><abc>Blah</abc>", 3, markuponly=1)
    assertlex("<abc>Blah&foo;Blah</abc>", 3)
    assertlex("<abc>Blah&foo;Blah</abc>", 2, markuponly=1)
    assertlex("<abc><abc>", 2)
    assertlex("</abc></abc>", 2)
    assertlex("<abc></def></abc>", 3)

if __name__=="__main__":
    testlexer()
