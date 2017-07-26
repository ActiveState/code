try:
    path='cn=people,ou=office,o=company'
    l=ldap.open('hostname')
    #set which protocol if you do not like the default
    l.protocol_version = ldap.VERSION2
    l.simple_bind('cn=root,ou=office,o=company','password')

    #search for surnames beginning with a
    #available options for how deep a search you want.
    #LDAP_SCOPE_BASE, LDAP_SCOPE_ONELEVEL,LDAP_SCOPE_SUBTREE,
    a=l.search_s(path,ldap.SCOPE_SUBTREE,'sn='+'a*')

    #delete fred
    l.delete_s('cn=fred,'+path)

    #add barney
    #note: objectclass is dependant on the ldap server
    user_info = {'uid':'barney123',
                'givenname':'Barney',
                'cn':'barney123',
                'sn':'Smith',
                'telephonenumber':'123-4567',
                'facsimiletelephonenumber':'987-6543',
                'objectclass':('Remote-Address','person', 'Top'),
                'physicaldeliveryofficename':'Services',
                'mail':'fred123@company.com',
                'title':'programmer',
                }

    id='cn=barney,'+path
    attributes=[ (k,v) for k,v in user_info.items() ]
    l.add_s(id,attributes)    
except ldap.LDAPError, error:
    print 'problem with ldap',error
     
