import urllib
import re
import os
 
path = "set your path or '.'"
i = 1
content = True
while content:
        dir = os.listdir(path)
        for file in dir:
                if file[:-4].isdigit():
                        if int(file[:-4]) >= i:
                                i = int(file[:-4])+1
        while content:
                url = "http://www.xkcd.com/"+str(i)+"/"
                rd = urllib.urlopen(url)
                data = rd.read()
                res = re.search("/comics/[a-z0-9_()]*.(jpg|png)", data)
                if res:
                        imgurl = "http://imgs.xkcd.com"+res.group()
                        image = urllib.URLopener()
                        image.retrieve(imgurl, path+str(i)+imgurl[-4:])
                else:
                        if re.search("Not Found", data) and i != 404:
                                content = False
                i += 1
