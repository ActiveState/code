import win32com,win32com.client,pythoncom
import time,os,string

def code_tup(l=''):
    return string.join(l,"','")
    

#get base LDAP string
ldap_loc=win32com.client.GetObject('LDAP://rootDSE').Get("defaultNamingContext")

print 'Found the following:'
print '\tbase ldap string: ',ldap_loc

#get exchange site
ldap_ex='CN=Microsoft Exchange,CN=Services,CN=Configuration'

ex_sites=[]
msg=''
try:
    for i in win32com.client.GetObject('LDAP://'+ldap_ex+','+ldap_loc):
        if i.cn!='Active Directory Connections': ex_sites.append(i.cn)
except pythoncom.com_error,(hr,msg,exc,arg):
    pass

if msg:
    print 'Failed on first attempt contacting exchange in Active Directory at\n',ldap_loc,'\n',msg
    ldap_loc=string.join(ldap_loc.split(',')[1:],',')
    print 'Now trying',ldap_loc    
    try:
        for i in win32com.client.GetObject('LDAP://'+ldap_ex+','+ldap_loc):
            if i.cn!='Active Directory Connections': ex_sites.append(i.cn)
    except pythoncom.com_error,(hr,msg,exc,arg):
        print msg
        print 'Cannot find exchange',sys.exit(1)
    
print '\tSites are:',string.join(ex_sites)
ex_server=[]
for ex_site in ex_sites:
    print 'At',ex_site
    ####get the exchange servers
    ex_admin_grps='CN=Administrative Groups,cn='+ex_site+','+ldap_ex+','+ldap_loc
    try:
        admin_grp=win32com.client.GetObject('LDAP://'+ex_admin_grps)[0].cn
    except pythoncom.com_error,(hr,msg,exc,arg):
        print 'Cannot find an Administrative Group',msg,'\nAt ',ex_admin_grps
        continue


    print '  Administrative Group:',admin_grp
    
    ldap_ex_srv='CN=Servers,'+'cn='+admin_grp+','+ex_admin_grps

    ex_servers=[]
  
    for server in win32com.client.GetObject('LDAP://'+ldap_ex_srv):
        ex_servers.append(server.cn)
    print '  Exchange servers:',string.join(ex_servers)

    ####get the information stores 
           ldap_info_store='CN=InformationStore,CN=%s,CN=Servers,CN=%s,%s'%(ex_servers[-1],admin_grp,ex_admin_grps)
    ex_stores=[]
    for info_store in win32com.client.GetObject('LDAP://'+ldap_info_store):
        print '    At Information store:',info_store.cn
        ldap_store='CN='+info_store.cn+','+ldap_info_store

        for store in win32com.client.GetObject('LDAP://'+ldap_store):
            print '      Store:',store.cn
            ex_stores.append('cn='+store.cn+','+ldap_store)

        
    #save it to a file:
    
    config_file='Ad_config_'+ex_site.lower()+'.py'
    if os.path.exists(config_file):
        os.rename(config_file,config_file+'_'+str(int(time.time()))+'.txt')
    f=open(config_file,'w')

    f.write("ldap_loc='%s'\n"%(ldap_loc))
    f.write("ex_site='%s'\n"%(ex_sites[0]))        
    f.write("ex_servers=('%s')\n\n"%(code_tup(ex_servers)))
    f.write("ex_stores=('%s')\n\n"%(code_tup(ex_stores)))
    #find mailbox store:
    found=0
    ex_mail_stores=[]
    for i in ex_stores:
        if i.find('Mailbox Store')!=-1: ex_mail_stores.append(i)
        found=1
    if not(found):
        f.write("ex_mail_stores='???%s\n\n'\n\n"%(ex_stores[0]))
    else:
        f.write("ex_mail_store=('%s')"%(code_tup(ex_mail_stores)))
    f.close()
