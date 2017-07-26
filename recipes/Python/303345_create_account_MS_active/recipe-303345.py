import win32com,win32com.client
def add_acct(location,account):
  ad_obj=win32com.client.GetObject(location)

  ad_user=ad_obj.Create('user','cn='+user['login'])
  ad_user.Put('sAMAccountName',user['login'])
  ad_user.Put('userPrincipalName',user['login']+'@email.address.com')
  ad_user.Put('DisplayName',user['last']+' '+user['first']) #fullname
  ad_user.Put('givenName',user['first'])
  ad_user.Put('sn',user['last'])
  ad_user.Put('description','regular account')
  ad_user.Put('physicalDeliveryOfficeName','office 1')
  ad_user.Extensionattribute10='your own attribute'
  ad_user.Put('HomeDirectory',r'\\server1\ '[:-1]+user['login']) 
  ad_user.Put('HomeDrive','H:')
  ad_user.SetInfo();ad_user.GetInfo()
  ad_user.LoginScript='login.bat'
  ad_user.AccountDisabled=0
  ad_user.setpassword('the password')
  ad_user.Put('pwdLastSet',0) #-- force reset of password
  ad_user.SetInfo()


location='LDAP://OU=org1,DC=company,DC=com'
user={'first':'fred','last':'smith','login':'fred123'}
add_acct(location,user)
