'''
ARFF2DB.py - ARFF to Database importer
Author: Pradeep Kishore Gowda <pradeep _at_ btbytes (dot) com>
Revision: 1.2
Changelog:
1.2 : rewritten from scratch using Pyparsing module and SQLAlchemy for db independence

Dependencies: SQLAlchemy, Pyparsing
'''
from pyparsing import *
from sqlalchemy import *


def ARFF2DB(data, connection, tblname): 
    #parse the data read from the ARFF file    
    arffFormat = Forward()
    E = CaselessLiteral("E")
    comment = '%' + restOfLine    
    relationToken = Keyword('@RELATION', caseless=True)
    dataToken = Keyword('@DATA', caseless=True)
    attribToken = Keyword('@ATTRIBUTE', caseless=True)
    ident = Word( alphas, alphanums + '_-' ).setName('identifier')    
    relation = Suppress(relationToken) \
               + ident.setResultsName('relation')    
    classDomain = Suppress('{') \
                  + Group(delimitedList(ident.setResultsName('domain'))).setResultsName('domains') + Suppress('}')
    attribute = Group(Suppress(attribToken) 
                + Word(alphas).setResultsName('attrname')+restOfLine).setResultsName('attribute')
    continuous = Group( attribute 
                 + Word(alphas).setResultsName('type'))
    discrete = Group(attribute + classDomain)                
    arithSign = Word("+-",exact=1)            
    realNum = Combine( Optional(arithSign) 
              + (Word( nums ) + "." + Optional( Word(nums) )|( "." + Word(nums) )) 
              + Optional( E + Optional(arithSign) + Word(nums) ))            
    dataList = Group(delimitedList(realNum|ident)).setResultsName('record') 
    arffFormat << ( relation
                   + OneOrMore(attribute).setResultsName('attributes')                  
                   + dataToken
                   + OneOrMore(dataList).setResultsName('records')).setResultsName('arffdata')

    simpleARFF = arffFormat
    simpleARFF.ignore(comment)
    tokens =  simpleARFF.parseString(data)    
    
    #write the data into the database
    db = create_engine(connection)
    metadata = BoundMetaData(db)
    
    if tblname:        
        table_name = tblname
    else:
        table_name = tokens.relation
        
    tbl = Table(table_name, metadata)
    for attr in tokens.attributes:
        if (attr.type=='REAL'):
            col = Column(attr.attrname, Numeric)
        else:
            col = Column(attr.attrname, String(50))
        tbl.columns.add(col)
    tbl.create()

    ins = tbl.insert()
    for record in tokens.records:
        dict = {}
        i = 0 
        for attr in tokens.attributes:
            dict.update({attr.attrname:record[i]})
            i +=1
        ins.execute(dict)
    
    
if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser()
    
    parser.add_option('-f', '--file',
                      action='store', type='string', dest='filename',
                      help='the arff file name', metavar="FILE")

    parser.add_option('-c', '--connection',
                      action='store', type='string', dest='connection',
                      help='Connection String Eg:mysql://user:pass@localhost:port/dbname>')
                      
    parser.add_option('-t', '--table',
                      action='store', type='string', dest='table',
                      help='Table name')
    (options, args) = parser.parse_args()          
    
    
    if options.filename and options.connection:
        text = ''.join(open(options.filename, 'r').readlines())
        ARFF2DB(text, options.connection, options.table)
    else:
        parser.print_help()
