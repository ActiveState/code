""" Script to enumerate the members of groups in the domain"""
import sys
from win32com.client import *

## The values should be the groups you wish to examine, use the group's sAMAccountName
groups = ['Administrators', 'Account Operators', 'Backup Operators',
            'Server Operators', 'DnsAdmins', 'Domain Admins', 
            'Exchange Administrators', 'Exchange Services', 
            'DHCP Administrators']

# Select the AD attributes you wish the query to return
attribs = "name,member,objectClass,adspath,primaryGroupToken,primaryGroupID"
objConnection = Dispatch("ADODB.Connection")
objConnection.Open("Provider=ADsDSOObject")

def getDefaultDN(server=None):
    """ Get the base LDAP Naming Context, used specified server if available."""

    if server is None:
        ldap_root = GetObject('LDAP://rootDSE')
    else:
        ldap_root = GetObject('LDAP://%s/rootDSE' % server)

    ldap_loc = ldap_root.Get('defaultNamingContext')

    return ldap_loc

def getGrpInfo(name, searchRoot, category="Group"):
    """ Find the group in AD and set up a dictionary for its attributes.
    
    searchRoot is the part of the LDAP tree that you want to start searching from.
    category filters what objedts to search on.  So you could also search for a User.
    name is the account's sAMAccountName which is a unique identifier in AD.
    attribs is the list of attributes to return from the query.
    """
    strSearch = \
        "<LDAP://%s>;(&(objectCategory=%s)(sAMAccountName=%s));%s;subtree" % \
        (searchRoot, category, name, attribs)
    objRecordSet = objConnection.Execute(strSearch)[0]
    objRecord = dict()

    # Normally, we would only expect one object to be retrieved.
    if objRecordSet.RecordCount == 1:
        # Set up a dictionary with attribute/value pairs and return the dictionary.
        for f in objRecordSet.Fields:
            objRecord[f.Name] = f.Value

        #print objRecord.items()
        return objRecord
    else:
        # Group not found
        return None

def getGrpMembers(strLdap, header=""):
    """ Recursively look up a group's members.
    
    strLdap is the groups adspath attribute.
    header is used for indenting to show sub groups.
    """
    strSearch = "<%s>;;%s" % (strLdap, attribs)
    objRecordSet = objConnection.Execute(strSearch)[0]
    objRecord = dict()
    memberList = []

    # Normally, we would only expect one object to be retrieved.
    if objRecordSet.RecordCount == 1:
        for f in objRecordSet.Fields:
            objRecord[f.Name] = f.Value

        # Check to see if the group has any members
        if objRecord['member'] is not None:
            # Look up each member and get their LDAP object
            for mbr in objRecord['member']:
                objRS = objConnection.Execute("<LDAP://%s>;;name,objectClass,adspath" % mbr)[0]

                # Check to see if the member is a group.
                # If so, look up its members.
                # The Field index number corresponds to the order that you list the
                # attributes in on the LDAP query string.
                if 'group' in objRS.Fields[1].Value:
                    memberList.append("%sGroup - %s, members:" % (header, objRS.Fields[0].Value))
                    memberList.extend(getGrpMembers(objRS.Fields[2].Value, header+"   "))
                else:
                    memberList.append("%s%s" % (header, objRS.Fields[0].Value))
        
    # Return the list of results
    return memberList

def getPrimaryGroup(searchRoot, token, header="   "):
    """ Used to look up Users whose Primary Group is set to one of the groups we're
    looking up.  This is necessary as AD uses that attribute to calculate a group's
    membership.  These type of users do not show up if you query the group's member field
    directly.
    
    searchRoot is the part of the LDAP tree that you want to start searching from.
    token is the groups primaryGroupToken.
    """
    strSearch = \
        "<LDAP://%s>;(primaryGroupID=%d);name;subtree" % \
        (searchRoot, token)
    objRecordSet = objConnection.Execute(strSearch)[0]
    memberList = []

    # Process if accounts are found.
    if objRecordSet.RecordCount > 0:
        memberList.append("Primary Group calculated:")
        objRecordSet.MoveFirst()

        while not objRecordSet.EOF:
            memberList.append("%s%s" % (header, objRecordSet.Fields[0].Value))
            objRecordSet.MoveNext()
            
    # Return the list of results
    return memberList

def main(server=None):
    """ Main program logic. """
    dn = getDefaultDN(server)
    message = []

    for grp in groups:
        objGrp = getGrpInfo(grp, dn)
        # If the group is found, process the group's membership.
        if objGrp is not None:
            message.append("\nMembers of %s:" % objGrp['name'])
            message.extend(getGrpMembers(objGrp['adspath']))
            message.extend(getPrimaryGroup(dn, objGrp['primaryGroupToken']))    
            
    print "\n".join(message)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        main()
    else:
        # If a server is given on the command line, run the script against it.
        main(sys.argv[1])
