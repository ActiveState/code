#!/usr/bin/env python
import DCOracle2,sys

def describe(connStr,table): 
 db=None
 try:
  db=DCOracle2.connect(connStr)
  dd=db.describe(table)

  fmt='%-20s\t%-10s\t%-10s' 
  typeFmt='%s(%s)'
  print fmt % ('Name','Null?','Type')
  print fmt % ('-'*20,'-'*10,'-'*10)
  for col in dd['OCI_ATTR_LIST_COLUMNS']:
    nullable=col['OCI_ATTR_IS_NULL']
    null=''
    if (not nullable): null='NOT NULL'
    type=typeFmt % (DCOracle2.Type(col['OCI_ATTR_DATA_TYPE']),col['OCI_ATTR_DATA_SIZE'])
    print fmt % (col['OCI_ATTR_NAME'],null,type)  
 finally:
   if db!=None:
	print 'close db'
   	db.close()

if __name__=='__main__':
 try:
   if (len(sys.argv)==3):
	describe(sys.argv[1],sys.argv[2])	
   else:
	print 'usage: desc.py <connection string> <table name>'
	print '       such as desc.py scott/tiger orders     '
 except:
	print 'Unexpected error:', sys.exc_info()[1]
