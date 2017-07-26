import os
import urllib2
import urllib
from urlparse import urlparse
from bs4 import BeautifulSoup
import easygui as eg


eg.msgbox("Search/Enter proper url"+'\n'+"Ex:naruto 100 or bleach 400"+'\n'+" www.mangareader.net/naruto/100",title="Manga Downloader", ok_button="ok")
q=eg.enterbox(msg='Search or Enter the Link.',title='Manga Downloader')
print q

def user_input(q):
    if 'www' in q:
        site1(q)
    else:
        search(q)

def search(query):
    """Name episod
    Ex: 1.Bleach 544
         2.Naruto 100"""

    s=query.lower().strip(' ').split(' ')
        
    link='http://www.mangareader.net/'+s[0]+'/'+s[1]
    if len(s) > 2:
        link='http://www.mangareader.net/'+'-'.join(s[0:-1])+'/'+s[-1]

    site1(link)


def site1(link):
    link=link.strip('http://')
    link=link.strip('.html')
    if (link.count('/')>2):
        print 'link.count:',link.count('/')

        two=link.find('/',20)
        three=link.find('/',two+1)
        #link=http://www.mangareader.net/440-45521-1/watashi-ni-xx-shinasai/chapter-8.html
        link='http://www.mangareader.net/'+link[two+1:three]+'/'+link[three+9:]
        print link

    if 'http://' not in link:
        
        link1="http://"+link
    else:
        link1=link
    
    try:
        html=urllib2.urlopen(link1).read()

    except urllib2.HTTPError:
        print('Enter proper url')
    
    soup = BeautifulSoup(html)
    link_image=soup.img['src']
    link_next=soup.img.parent['href']
    """ Creates folder at specified location"""
    link_properties = urlparse(link)
    start=link_properties.path.find('/')
    end=link_properties.path.find('/',start+1)
    folder_name=link_properties.path[start+1:end]+'_'+link_properties.path[end+1:]
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    """Completed creating Directory"""
        
    
    
    if 'www.' in link_next:
        pass
    link_next='http://www.mangareader.net'+link_next
    i=0
    while ('/'+link_properties.path[end+1:]+'/')in link_image:
        
            f = open(folder_name+'/'+str(i+1)+'.jpg','wb')
            f.write(urllib.urlopen(link_image).read())
            f.close()
            html=urllib2.urlopen(link_next).read()
            soup = BeautifulSoup(html)
            link_image=soup.img['src']
            link_next=soup.img.parent['href']
            link_next='http://www.mangareader.net'+link_next
            print link_next,link_image
            i=i+1

#search("one piece 100")
user_input(q)
