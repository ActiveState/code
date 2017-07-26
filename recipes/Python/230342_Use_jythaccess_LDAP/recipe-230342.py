from javax.naming import *
from java.util import *
from javax.naming.directory import *
class ADS:
    '''
    The parameters required for making the connections.
    the user name should be a user with previliges to log into the
    LDAP machine.
    '''
    ads_server="<adsserver>"
    ads_user="<valid_username>"
    ads_password="<valid_password>"
    ads_base_dns="DC=something,DC=com"
    '''
        The constructor: This intialises the ads object 
    '''
    def __init__(self):
        self.url="ldap://%s/%s" % (self.ads_server,self.ads_base_dns)
        env=Hashtable()
        env.put(Context.INITIAL_CONTEXT_FACTORY, "com.sun.jndi.ldap.LdapCtxFactory")
        env.put(Context.PROVIDER_URL, self.url)
        env.put(Context.SECURITY_AUTHENTICATION, "simple")
        env.put(Context.SECURITY_PRINCIPAL, self.ads_user)
        env.put(Context.SECURITY_CREDENTIALS, self.ads_password)
        ctx =InitialDirContext(env)
        self.ctx=ctx
    '''
        The string method is overriden to print the url used to connect to the ads server.
    '''
    def __str__(self):
        return self.url
    '''
    Method for adding an attribute with a specific value to ADS
    '''
    def modify_attribute(self,name,value,username=None):
        myAttrs = BasicAttributes(1)
        oc = BasicAttribute(name)
        oc.add(value)
        myAttrs.put(oc)
        if username!=None:
            self.ctx.modifyAttributes("cn=%s,ou=portal,ou=admins" % username, DirContext.REPLACE_ATTRIBUTE, myAttrs)
        else:
            results=self.search_user("*")
            for result in results:
                attrs=result.getAttributes()
                try:
                    self.ctx.modifyAttributes("cn=%s,ou=portal,ou=admins" % attrs.get("name").get(), DirContext.REPLACE_ATTRIBUTE, myAttrs)
                except:
                    pass
    '''
    Method for searching a user by it's name for wild card search use *
    '''
    def search_user(self,username):
        return self.search(username,"user")
    '''
    Method for searching a group by it's name for wild card search user *
    '''
    def search_group(self,groupname):
        return self.search(groupname,"group")
    '''
    The main search class
    '''
    def search(self,criteria,objectclass):
        srch =SearchControls()
        srch.setSearchScope(SearchControls.SUBTREE_SCOPE)
        results = self.ctx.search("", "(&(CN=%s) (objectClass=%s))" % (criteria,objectclass), srch)
        return results
        
'''
The class for handling the output results of the ads search
'''
class Output:
    '''
    Method for printing all the attributes present in the search result
    of a user or group.
    '''
    def print_attributes(self,results):
        for result in results:
            attributes=result.getAttributes()
            
            for atr in attributes.getIDs():
                print str(atr)
    '''
    Method for printing the values of results in ADS.
    '''
    def print(self,results,*attributes):
        for result in results:
            ads_attributes=result.getAttributes()
            print self.attribute_string(ads_attributes,attributes)
    '''
    Method for writing the results of the the output to a file
    '''
    def log(self,results,*attributes):
        filename="output.ads"
        fd=open(filename,"w")
        for result in results:
            ads_attributes=result.getAttributes()        
            fd.write("%s\n" % self.attribute_string(ads_attributes,attributes))
        fd.flush()
        fd.close()
    '''
    Generic method for displaying the ADS attribute
    '''
    def attribute_string(self,ads_attributes,attributes):
        result=str(ads_attributes.get("name"))
        for attribute in attributes:
            result="%s,%s" % (result,ads_attributes.get(attribute))
        return result
