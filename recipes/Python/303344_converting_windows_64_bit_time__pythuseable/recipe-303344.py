import time

def conv_time(l,h):
    #converts 64-bit integer specifying the number of 100-nanosecond
    #intervals which have passed since January 1, 1601.
    #This 64-bit value is split into the
    #two 32 bits  stored in the structure.
    d=116444736000000000L #difference between 1601 and 1970
    #we divide by 10million to convert to seconds
    return (((long(h)<< 32) + long(l))-d)/10000000    

For example, active directory in windows uses this time to note when a password was last set.

If you have a com object representing a user in active directory:
user='LDAP://cn=fred,OU=office1,DC=company,DC=com'
user_obj=win32com.client.GetObject(user)

To get the time the password was last set you would do the following:
print conv_time(user.pwdLastSet.lowpart,user.pwdLastSet.highpart) 
