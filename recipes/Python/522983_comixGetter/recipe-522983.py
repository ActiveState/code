'''
comixGetter.py - a python script to download daily comics from ucomics and comics .com's
author: sami
date: mar 07
todo: a. check if file already exists, b. save with correct file extension
'''

import httplib, re

re_date = '[a-zA-Z]+,\s+(\d+)\s+([a-zA-Z]+)\s+(\d+).+'

dates = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06', 
         'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}

comics_dot_com_info = (
              ('peanuts', '/comics/', '.+(\/comics\/peanuts\/archive\/images\/peanuts\d+\.gif|\/comics\/peanuts\/archive\/images\/peanuts\d+\.jpg).+'),
              ('dilbert', '/comics/', '.+(\/comics\/dilbert\/archive\/images\/dilbert\d+\.gif|\/comics\/dilbert\/archive\/images\/dilbert\d+\.jpg).+'),
              ('bignate', '/comics/', '.+(\/comics\/bignate\/archive\/images\/bignate\d+\.gif|\/comics\/bignate\/archive\/images\/bignate\d+\.jpg).+'),
              ('drabble', '/comics/', '.+(\/comics\/drabble\/archive\/images\/drabble\d+\.gif|\/comics\/drabble\/archive\/images\/drabble\d+\.jpg).+'),
              ('franknernest', '/comics/', '.+(\/comics\/franknernest\/archive\/images\/franknernest\d+\.jpg).+'),
              ('monty', '/comics/', '.+(\/comics\/monty\/archive\/images\/monty\d+\.gif|\/comics\/monty\/archive\/images\/monty\d+\.jpg).+'),
              ('wizardofid', '/creators/', '.+(\/creators\/wizardofid\/archive\/images\/wizardofid\d+\.gif|\/creators\/wizardofid\/archive\/images\/wizardofid\d+\.jpg).+'),
             )

ucomics_dot_com_info = (
              ('doonesbury', '/comics/db/', 'db'),
              ('calvin_and_hobbes', '/comics/ch/', 'ch')
             )

#===============================
#download_others - random comic downloads
#
#===============================
def download_others():
    
    cnxn = connect('www.archiecomics.com')
    
    print "getting: Archie"
    
    cnxn.request("GET", '/')
    
    res = cnxn.getresponse()
            
    p = re.match(re_date, res.getheader("date"))
        
    comic_path = '/pops_shop/dailycomics/image' + p.group(1) + '.gif'
    
    #reconnecting since archiecomics.com closes connection after sending response
    cnxn = connect('www.archiecomics.com')
    
    cnxn.request("GET", comic_path)
                        
    res = cnxn.getresponse()
    
    igot = res.status, res.reason

    if res.status != "200" and res.reason != "OK":
      print 'continuing to next comic since i got: '
      print igot
      return
              
    f = open('archie'+"_"+p.group(1)+"_"+p.group(2)+"_"+p.group(3)+".gif", "wb")

    f.write(res.read())
    
    f.close()
    
    print "OK" 

#===============================
#connect(server) - connect to server
#
#===============================             
def connect(server):
    con = httplib.HTTPConnection(server, 80)
    con.connect()                                                      
    #print con
    return con

#===============================
#download_ucomics_dot_com - download comics from ucomics/gocomics servers
#
#===============================
def download_ucomics_dot_com():
        
    cnxn = connect('images.ucomics.com')
    
    cnxn.request("GET", '/')
    
    res = cnxn.getresponse()
        
    p = re.match(re_date, res.getheader("date"))
        
    for entry in ucomics_dot_com_info:
            
        print "getting: " + entry[0]
        
        comic_path = entry[1] + p.group(3) + '/'+ entry[2] + p.group(3)[2] + p.group(3)[3] + dates[p.group(2)] + p.group(1) + '.gif';
        
        #for ucomics.com, we need to reconnect everytime, server closes connection after sending a response        
        cnxn = connect('images.ucomics.com')
        
        cnxn.request("GET", comic_path)
                        
        res = cnxn.getresponse()
                        
        igot = res.status, res.reason
  
        if res.status != "200" and res.reason != "OK":
          print 'continuing to next comic since i got: '
          print igot
          continue
          
        f = open(entry[0]+"_"+p.group(1)+"_"+p.group(2)+"_"+p.group(3)+".gif", "wb")

        f.write(res.read())
        
        f.close()
        
        print "OK"  

#===============================
#download_comics_dot_com - download comics from comics.com servers
#
#===============================
def download_comics_dot_com():

    #Calling connect to url directly since for comics.com, the server does not close the connection itself after
    #sending a response
    cnxn = connect('comics.com')
    
    for entry in comics_dot_com_info:
      
      print "getting: " + entry[0]
            
      cnxn.request("GET", entry[1]+entry[0]+'/')
      
      res = cnxn.getresponse()
      igot = res.status, res.reason
      if res.status != "200" and res.reason != "OK":
        print 'continuing to next comic since i got: '
        print igot
        continue
      
      p = re.match(re_date, res.getheader("date"))
      
      iread = res.read()
      l = re.findall(entry[2], iread)
                 
      cnxn.request("GET", l[0])
      res = cnxn.getresponse()
      
      f = open(entry[0]+"_"+p.group(1)+"_"+p.group(2)+"_"+p.group(3)+".gif", "wb")

      f.write(res.read())
      
      f.close()
      
      print "OK"

#===============================
#execution
#
#===============================
download_comics_dot_com()
download_ucomics_dot_com()
download_others()
