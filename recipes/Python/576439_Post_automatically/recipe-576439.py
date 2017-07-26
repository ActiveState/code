import urllib
import httplib2
"""
A little script to post automatically a recipe to the cookbook
it need :
thanks to http://code.google.com/p/httplib2/
Bussiere @at gmail.com

"""

def post_cookbook(login,password,title,description,tags,code,discussion):
    http = httplib2.Http()
    url = 'http://login.activestate.com/signin/?next=http%3A%2F%2Fcode.activestate.com%2Frecipes%2Flangs%2Fpython%2F'   
    body = {'email': login, 'password': password}
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    response, content = http.request(url, 'POST', headers=headers, body=urllib.urlencode(body))
    
    headers = {'Cookie': response['set-cookie'],'Content-type': 'application/x-www-form-urlencoded'}
    #lang : 1 is for python langage
    body = {'title': title, 'description': description,'tags':tags,'lang':1,'code' : code,'discussion':discussion}
    url = 'http://code.activestate.com/recipes/add/'   
    response, content = http.request(url, 'POST', headers=headers,body=urllib.urlencode(body))


if __name__ == "__main__":
    post_cookbook('login','password','titre','description','tags tag','print booh','discussion')
