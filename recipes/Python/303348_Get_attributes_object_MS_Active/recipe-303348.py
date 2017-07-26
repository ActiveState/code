import win32com,win32com.client

def ad_dict(ldap_path,value_required=1):
  attr_dict={}
  adobj=win32com.client.GetObject(ldap_path)
  schema_obj=win32com.client.GetObject(adobj.schema)
  for i in schema_obj.MandatoryProperties:
      value=getattr(adobj,i)
      if value_required and value==None: continue
      attr_dict[i]=value
  for i in schema_obj.OptionalProperties:
      value=getattr(adobj,i)
      if value_required and value==None: continue
      attr_dict[i]=value
  return attr_dict


user='LDAP://cn=fred123,OU=people,DC=company,DC=com'

print ad_dict(user)
