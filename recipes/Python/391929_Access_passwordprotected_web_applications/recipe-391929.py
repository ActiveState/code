import sys
sys.path.append('ClientCookie-1.0.3')
import ClientCookie
sys.path.append('ClientForm-0.1.17')
import ClientForm

# Create special URL opener (for User-Agent) and cookieJar
cookieJar = ClientCookie.CookieJar()

opener = ClientCookie.build_opener(ClientCookie.HTTPCookieProcessor(cookieJar))
opener.addheaders = [("User-agent","Mozilla/5.0 (compatible)")]
ClientCookie.install_opener(opener)
fp = ClientCookie.urlopen("http://login.yahoo.com")
forms = ClientForm.ParseResponse(fp)
fp.close()

# print forms on this page
for form in forms: 
    print "***************************"
    print form

form = forms[0]
form["login"]  = "yahoo-user-id" # use your userid
form["passwd"] = "password"      # use your password
fp = ClientCookie.urlopen(form.click())
fp.close()
fp = ClientCookie.urlopen("http://groups.yahoo.com/group/mygroup") # use your group
fp.readlines()
fp.close()
